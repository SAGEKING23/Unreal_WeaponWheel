#include "WeaponWheelWidget.h"
#include "WeaponInventoryComponent.h"
#include "Components/CanvasPanelSlot.h"
#include "Components/Image.h"
#include "Components/TextBlock.h"
#include "Components/ProgressBar.h"
#include "Engine/Texture2D.h"
#include "Animation/WidgetAnimation.h"
#include "TimerManager.h"

void UWeaponWheelWidget::NativeConstruct()
{
	Super::NativeConstruct();

	if (WheelCanvas)
	{
		WheelCanvas->SetVisibility(ESlateVisibility::Visible);
	}

	CreateSlotWidgets();
	PlayOpenAnimation();
}

void UWeaponWheelWidget::NativeDestruct()
{
	Super::NativeDestruct();
}

void UWeaponWheelWidget::NativeTick(const FGeometry& MyGeometry, float InDeltaTime)
{
	Super::NativeTick(MyGeometry, InDeltaTime);

	if (bIsOpening)
	{
		AnimationProgress += InDeltaTime * 4.0f; // 0.25s animation
		if (AnimationProgress >= 1.0f)
		{
			AnimationProgress = 1.0f;
			bIsOpening = false;
		}
		UpdateWheel();
	}
	else if (bIsClosing)
	{
		AnimationProgress -= InDeltaTime * 4.0f;
		if (AnimationProgress <= 0.0f)
		{
			AnimationProgress = 0.0f;
			bIsClosing = false;
			SetVisibility(ESlateVisibility::Collapsed);
		}
		UpdateWheel();
	}
}

void UWeaponWheelWidget::InitializeWidget(UWeaponInventoryComponent* InInventoryComponent)
{
	InventoryComponent = InInventoryComponent;

	if (InventoryComponent && InventoryComponent->GetWeaponWheelConfig())
	{
		NumSlots = FMath::Min(InventoryComponent->GetWeaponWheelConfig()->MaxVisibleSlots, 8);
		WheelRadius = InventoryComponent->GetWeaponWheelConfig()->WheelRadius;
	}

	UpdateWheel();
}

void UWeaponWheelWidget::UpdateWheel()
{
	if (!InventoryComponent) return;

	const TArray<FWeaponSlotData>& Slots = InventoryComponent->GetAllWeaponSlots();
	NumSlots = FMath::Min(Slots.Num(), NumSlots);

	// Update slot visuals
	for (int32 i = 0; i < NumSlots; ++i)
	{
		UpdateSlotVisuals(i);
	}

	// Update center display
	UpdateCenterDisplay();
}

void UWeaponWheelWidget::CreateSlotWidgets()
{
	if (!WheelCanvas) return;

	// Clear existing
	for (UCanvasPanel* Container : SlotContainers)
	{
		if (Container)
		{
			Container->RemoveFromParent();
		}
	}
	SlotContainers.Empty();
	SlotIcons.Empty();
	SlotLabels.Empty();
	SlotBackgrounds.Empty();
	SlotAmmoBars.Empty();

	// Create slot containers
	for (int32 i = 0; i < 8; ++i) // Max 8 slots
	{
		UCanvasPanel* Container = NewObject<UCanvasPanel>(WheelCanvas);
		Container->SetVisibility(ESlateVisibility::Visible);
		WheelCanvas->AddChild(Container);

		UCanvasPanelSlot* ContainerSlot = Cast<UCanvasPanelSlot>(Container->Slot);
		if (ContainerSlot)
		{
			ContainerSlot->SetAnchors(FAnchors(0.5f, 0.5f, 0.5f, 0.5f));
			ContainerSlot->SetAlignment(FVector2D(0.5f, 0.5f));
			ContainerSlot->SetSize(FVector2D(100.0f, 100.0f));
		}

		// Background
		UImage* Background = NewObject<UImage>(Container);
		Background->SetBrushSize(FVector2D(90.0f, 90.0f));
		Background->SetColorAndOpacity(FLinearColor(0.1f, 0.1f, 0.1f, 0.8f));
		Container->AddChild(Background);
		UCanvasPanelSlot* BgSlot = Cast<UCanvasPanelSlot>(Background->Slot);
		if (BgSlot)
		{
			BgSlot->SetAnchors(FAnchors(0.5f, 0.5f, 0.5f, 0.5f));
			BgSlot->SetAlignment(FVector2D(0.5f, 0.5f));
			BgSlot->SetPosition(FVector2D(0.0f, 0.0f));
		}

		// Icon
		UImage* Icon = NewObject<UImage>(Container);
		Icon->SetBrushSize(FVector2D(64.0f, 64.0f));
		Container->AddChild(Icon);
		UCanvasPanelSlot* IconSlot = Cast<UCanvasPanelSlot>(Icon->Slot);
		if (IconSlot)
		{
			IconSlot->SetAnchors(FAnchors(0.5f, 0.5f, 0.5f, 0.5f));
			IconSlot->SetAlignment(FVector2D(0.5f, 0.5f));
			IconSlot->SetPosition(FVector2D(0.0f, -10.0f));
		}

		// Label
		UTextBlock* Label = NewObject<UTextBlock>(Container);
		Label->SetFont(FSlateFontInfo(FCoreStyle::GetDefaultFontStyle("Bold", 12), 12));
		Label->SetColorAndOpacity(FLinearColor::White);
		Label->SetJustification(ETextJustify::Center);
		Container->AddChild(Label);
		UCanvasPanelSlot* LabelSlot = Cast<UCanvasPanelSlot>(Label->Slot);
		if (LabelSlot)
		{
			LabelSlot->SetAnchors(FAnchors(0.5f, 0.5f, 0.5f, 0.5f));
			LabelSlot->SetAlignment(FVector2D(0.5f, 0.5f));
			LabelSlot->SetPosition(FVector2D(0.0f, 35.0f));
		}

		// Ammo bar
		UProgressBar* AmmoBar = NewObject<UProgressBar>(Container);
		AmmoBar->SetFillColorAndOpacity(FLinearColor(0.2f, 0.8f, 0.2f, 0.8f));
		AmmoBar->SetBackgroundColor(FLinearColor(0.1f, 0.1f, 0.1f, 0.5f));
		AmmoBar->SetPercent(1.0f);
		AmmoBar->SetVisibility(ESlateVisibility::Visible);
		Container->AddChild(AmmoBar);
		UCanvasPanelSlot* BarSlot = Cast<UCanvasPanelSlot>(AmmoBar->Slot);
		if (BarSlot)
		{
			BarSlot->SetAnchors(FAnchors(0.5f, 0.5f, 0.5f, 0.5f));
			BarSlot->SetAlignment(FVector2D(0.5f, 0.5f));
			BarSlot->SetPosition(FVector2D(-40.0f, 55.0f));
			BarSlot->SetSize(FVector2D(80.0f, 6.0f));
		}

		SlotContainers.Add(Container);
		SlotBackgrounds.Add(Background);
		SlotIcons.Add(Icon);
		SlotLabels.Add(Label);
		SlotAmmoBars.Add(AmmoBar);
	}
}

void UWeaponWheelWidget::UpdateSlotVisuals(int32 SlotIndex)
{
	if (!InventoryComponent) return;
	if (!SlotContainers.IsValidIndex(SlotIndex)) return;

	const TArray<FWeaponSlotData>& Slots = InventoryComponent->GetAllWeaponSlots();
	if (!Slots.IsValidIndex(SlotIndex)) return;

	const FWeaponSlotData& Slot = Slots[SlotIndex];
	UCanvasPanel* Container = SlotContainers[SlotIndex];
	UImage* Background = SlotBackgrounds[SlotIndex];
	UImage* Icon = SlotIcons[SlotIndex];
	UTextBlock* Label = SlotLabels[SlotIndex];
	UProgressBar* AmmoBar = SlotAmmoBars[SlotIndex];

	if (!Container) return;

	// Calculate position
	FVector2D Position = CalculateSlotPosition(SlotIndex);
	Position.X *= AnimationProgress;
	Position.Y *= AnimationProgress;

	UCanvasPanelSlot* ContainerSlot = Cast<UCanvasPanelSlot>(Container->Slot);
	if (ContainerSlot)
	{
		ContainerSlot->SetPosition(Position);
	}

	// Update visuals based on state
	bool bIsHovered = (SlotIndex == HoveredSlotIndex);
	bool bIsSelected = (SlotIndex == SelectedSlotIndex);
	bool bIsCurrent = (SlotIndex == InventoryComponent->GetCurrentSlotIndex());
	bool bIsUnlocked = Slot.bIsUnlocked;
	bool bHasWeapons = Slot.AvailableWeapons.Num() > 0;

	// Background color
	FLinearColor BgColor;
	if (!bIsUnlocked)
	{
		BgColor = FLinearColor(0.2f, 0.2f, 0.2f, 0.5f);
	}
	else if (bIsHovered || bIsSelected)
	{
		BgColor = FLinearColor(0.0f, 0.5f, 1.0f, 0.9f);
	}
	else if (bIsCurrent)
	{
		BgColor = FLinearColor(0.0f, 0.8f, 0.3f, 0.8f);
	}
	else
	{
		BgColor = FLinearColor(0.1f, 0.1f, 0.1f, 0.8f);
	}

	if (Background)
	{
		Background->SetColorAndOpacity(BgColor);
		// Scale effect for hover
		if (bIsHovered)
		{
			Background->SetRenderScale(FVector2D(1.15f, 1.15f));
		}
		else
		{
			Background->SetRenderScale(FVector2D(1.0f, 1.0f));
		}
	}

	// Icon
	if (Icon && bHasWeapons)
	{
		const FWeaponClassData* CurrentWeapon = Slot.GetCurrentWeapon();
		if (CurrentWeapon && CurrentWeapon->IconTexture.IsValid())
		{
			UTexture2D* Texture = CurrentWeapon->IconTexture.LoadSynchronous();
			if (Texture)
			{
				Icon->SetBrushFromTexture(Texture);
				Icon->SetColorAndOpacity(FLinearColor::White);
			}
		}
		else
		{
			Icon->SetColorAndOpacity(FLinearColor(0.5f, 0.5f, 0.5f, 0.5f));
		}
	}
	else if (Icon)
	{
		Icon->SetColorAndOpacity(FLinearColor(0.3f, 0.3f, 0.3f, 0.3f));
	}

	// Label
	if (Label)
	{
		FText LabelText = Slot.SlotName.IsEmpty() ? FText::FromString(UEnum::GetValueAsString(Slot.Category)) : Slot.SlotName;
		if (!bIsUnlocked)
		{
			LabelText = FText::FromString("LOCKED");
		}
		Label->SetText(LabelText);

		if (bIsHovered || bIsSelected)
		{
			Label->SetColorAndOpacity(FLinearColor(1.0f, 1.0f, 1.0f, 1.0f));
		}
		else if (!bIsUnlocked)
		{
			Label->SetColorAndOpacity(FLinearColor(0.5f, 0.5f, 0.5f, 0.8f));
		}
		else
		{
			Label->SetColorAndOpacity(FLinearColor(0.8f, 0.8f, 0.8f, 0.8f));
		}
	}

	// Ammo bar
	if (AmmoBar && bHasWeapons)
	{
		const FWeaponClassData* CurrentWeapon = Slot.GetCurrentWeapon();
		if (CurrentWeapon && CurrentWeapon->MaxAmmo > 0)
		{
			float Percent = (float)CurrentWeapon->CurrentAmmo / (float)CurrentWeapon->MaxAmmo;
			AmmoBar->SetPercent(Percent);
			AmmoBar->SetVisibility(ESlateVisibility::Visible);
		}
		else
		{
			AmmoBar->SetVisibility(ESlateVisibility::Collapsed);
		}
	}
	else if (AmmoBar)
	{
		AmmoBar->SetVisibility(ESlateVisibility::Collapsed);
	}

	// Container visibility
	Container->SetVisibility(bIsUnlocked ? ESlateVisibility::Visible : ESlateVisibility::HitTestInvisible);
}

void UWeaponWheelWidget::UpdateCenterDisplay()
{
	if (!InventoryComponent) return;

	const FWeaponClassData* CurrentWeapon = InventoryComponent->GetCurrentWeapon();
	const FWeaponSlotData* CurrentSlot = InventoryComponent->GetWeaponSlotByIndex(InventoryComponent->GetCurrentSlotIndex());

	if (CenterIcon && CurrentWeapon && CurrentWeapon->IconTexture.IsValid())
	{
		UTexture2D* Texture = CurrentWeapon->IconTexture.LoadSynchronous();
		if (Texture)
		{
			CenterIcon->SetBrushFromTexture(Texture);
			CenterIcon->SetColorAndOpacity(FLinearColor::White);
		}
	}
	else if (CenterIcon)
	{
		CenterIcon->SetColorAndOpacity(FLinearColor(0.5f, 0.5f, 0.5f, 0.5f));
	}

	if (CenterWeaponName && CurrentWeapon)
	{
		CenterWeaponName->SetText(CurrentWeapon->DisplayName);
	}
	else if (CenterWeaponName && CurrentSlot)
	{
		CenterWeaponName->SetText(CurrentSlot->SlotName);
	}

	if (CenterAmmoText && CurrentWeapon && CurrentWeapon->MaxAmmo > 0)
	{
		FString AmmoText = FString::Printf(TEXT("%d / %d"), CurrentWeapon->CurrentAmmo, CurrentWeapon->ReserveAmmo);
		CenterAmmoText->SetText(FText::FromString(AmmoText));
	}
	else if (CenterAmmoText)
	{
		CenterAmmoText->SetText(FText::GetEmpty());
	}

	if (CenterAmmoBar && CurrentWeapon && CurrentWeapon->MaxAmmo > 0)
	{
		float Percent = (float)CurrentWeapon->CurrentAmmo / (float)CurrentWeapon->MaxAmmo;
		CenterAmmoBar->SetPercent(Percent);
	}
	else if (CenterAmmoBar)
	{
		CenterAmmoBar->SetPercent(0.0f);
	}
}

FVector2D UWeaponWheelWidget::CalculateSlotPosition(int32 SlotIndex) const
{
	if (NumSlots <= 1) return FVector2D::ZeroVector;

	const TArray<FWeaponSlotData>* SlotsPtr = InventoryComponent ? &InventoryComponent->GetAllWeaponSlots() : nullptr;
	float Angle = 0.0f;

	if (SlotsPtr && SlotsPtr->IsValidIndex(SlotIndex))
	{
		Angle = (*SlotsPtr)[SlotIndex].WheelAngle;
	}
	else
	{
		// Evenly distribute
		Angle = (360.0f / NumSlots) * SlotIndex - 90.0f; // Start at top
	}

	float Radians = FMath::DegreesToRadians(Angle);
	float X = FMath::Cos(Radians) * WheelRadius;
	float Y = FMath::Sin(Radians) * WheelRadius;

	return FVector2D(X, Y);
}

void UWeaponWheelWidget::SetHoveredSlot(int32 SlotIndex)
{
	HoveredSlotIndex = SlotIndex;
	UpdateWheel();
}

void UWeaponWheelWidget::SetSelectedSlot(int32 SlotIndex)
{
	SelectedSlotIndex = SlotIndex;
	UpdateWheel();
}

void UWeaponWheelWidget::HandleMouseWheel(float Delta)
{
	if (InventoryComponent)
	{
		InventoryComponent->OnCycleWeaponInput(Delta);
		UpdateWheel();
	}
}

void UWeaponWheelWidget::HandleConfirmSelection()
{
	if (InventoryComponent)
	{
		InventoryComponent->OnWeaponWheelConfirmSelection();
	}
}

void UWeaponWheelWidget::PlayOpenAnimation()
{
	bIsOpening = true;
	bIsClosing = false;
	AnimationProgress = 0.0f;
	SetVisibility(ESlateVisibility::Visible);

	if (OpenAnimation)
	{
		PlayAnimation(OpenAnimation);
	}
}

void UWeaponWheelWidget::PlayCloseAnimation()
{
	bIsClosing = true;
	bIsOpening = false;

	if (CloseAnimation)
	{
		PlayAnimation(CloseAnimation);
	}
}