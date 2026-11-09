#pragma once

#include "CoreMinimal.h"
#include "Blueprint/UserWidget.h"
#include "Components/CanvasPanel.h"
#include "Components/Image.h"
#include "Components/TextBlock.h"
#include "Components/ProgressBar.h"
#include "WeaponTypes.h"
#include "WeaponWheelWidget.generated.h"

class UWeaponInventoryComponent;
class UCanvasPanel;
class UImage;
class UTextBlock;
class UProgressBar;
class UWidgetAnimation;

/**
 * Widget for the weapon wheel UI
 */
UCLASS()
class MY_PROJECT_API UWeaponWheelWidget : public UUserWidget
{
	GENERATED_BODY()

public:
	virtual void NativeConstruct() override;
	virtual void NativeDestruct() override;
	virtual void NativeTick(const FGeometry& MyGeometry, float InDeltaTime) override;

	/** Initialize the widget with the inventory component */
	UFUNCTION(BlueprintCallable, Category = "Weapon Wheel")
	void InitializeWidget(UWeaponInventoryComponent* InInventoryComponent);

	/** Update the wheel display */
	UFUNCTION(BlueprintCallable, Category = "Weapon Wheel")
	void UpdateWheel();

	/** Set the hovered slot index */
	UFUNCTION(BlueprintCallable, Category = "Weapon Wheel")
	void SetHoveredSlot(int32 SlotIndex);

	/** Get the currently hovered slot index */
	UFUNCTION(BlueprintPure, Category = "Weapon Wheel")
	int32 GetHoveredSlot() const { return HoveredSlotIndex; }

	/** Set the selected slot index */
	UFUNCTION(BlueprintCallable, Category = "Weapon Wheel")
	void SetSelectedSlot(int32 SlotIndex);

	/** Handle mouse wheel for cycling weapons in current slot */
	UFUNCTION(BlueprintCallable, Category = "Weapon Wheel")
	void HandleMouseWheel(float Delta);

	/** Handle confirm selection (click/enter) */
	UFUNCTION(BlueprintCallable, Category = "Weapon Wheel")
	void HandleConfirmSelection();

protected:
	/** The inventory component reference */
	UPROPERTY()
	TObjectPtr<UWeaponInventoryComponent> InventoryComponent;

	/** Root canvas panel for the wheel */
	UPROPERTY(meta = (BindWidget))
	TObjectPtr<UCanvasPanel> WheelCanvas;

	/** Center display for current weapon info */
	UPROPERTY(meta = (BindWidget))
	TObjectPtr<UImage> CenterIcon;

	UPROPERTY(meta = (BindWidget))
	TObjectPtr<UTextBlock> CenterWeaponName;

	UPROPERTY(meta = (BindWidget))
	TObjectPtr<UTextBlock> CenterAmmoText;

	UPROPERTY(meta = (BindWidget))
	TObjectPtr<UProgressBar> CenterAmmoBar;

	/** Animation for wheel open/close */
	UPROPERTY(meta = (BindWidgetAnim))
	TObjectPtr<UWidgetAnimation> OpenAnimation;

	UPROPERTY(meta = (BindWidgetAnim))
	TObjectPtr<UWidgetAnimation> CloseAnimation;

	UPROPERTY(meta = (BindWidgetAnim))
	TObjectPtr<UWidgetAnimation> SlotHoverAnimation;

	UPROPERTY(meta = (BindWidgetAnim))
	TObjectPtr<UWidgetAnimation> SlotSelectAnimation;

private:
	/** Currently hovered slot index */
	int32 HoveredSlotIndex = -1;

	/** Currently selected slot index */
	int32 SelectedSlotIndex = 0;

	/** Slot widget containers */
	TArray<TObjectPtr<UCanvasPanel>> SlotContainers;
	TArray<TObjectPtr<UImage>> SlotIcons;
	TArray<TObjectPtr<UTextBlock>> SlotLabels;
	TArray<TObjectPtr<UImage>> SlotBackgrounds;
	TArray<TObjectPtr<UProgressBar>> SlotAmmoBars;

	/** Number of slots in the wheel */
	int32 NumSlots = 6;

	/** Wheel radius */
	float WheelRadius = 200.0f;

	/** Animation state */
	float AnimationProgress = 0.0f;
	bool bIsOpening = false;
	bool bIsClosing = false;

	/** Create slot widgets dynamically */
	void CreateSlotWidgets();

	/** Update slot widget visuals */
	void UpdateSlotVisuals(int32 SlotIndex);

	/** Update center display */
	void UpdateCenterDisplay();

	/** Calculate position for a slot on the wheel */
	FVector2D CalculateSlotPosition(int32 SlotIndex) const;

	/** Handle animation playback */
	void PlayOpenAnimation();
	void PlayCloseAnimation();
};