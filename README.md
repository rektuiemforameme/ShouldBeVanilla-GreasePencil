# ShouldBeVanilla-GreasePencil
Addon for Blender that provides some features for Grease Pencil editing that really should be in vanilla Blender.

## Features
### Batch Add Mask(s) and Batch Set Layer Property
Batch Add Mask(s) and Batch Set Layer Property allow you to add masks and change properties on multiple layers at once. They are available in the Layer Specials context menu:

![Layer Specials context menu](https://i.imgur.com/IExyLwZ.png)

Selecting one of these options will open a popup dialogue that will let you select the layers you want the operations to affect and the mask(s) to add or the property to change and what to change it to. You can select the layers to affect from the list. The buttons on the bottom left of the layer list change the selection. The left button will deselect all layers, the middle button will invert the selection and the right button will deselect all layers.

![Layer Selecting](https://i.imgur.com/qat3UVF.gif)

Below the layer selection area is the area to assign masks or change a property. The mask selection is a list, so you can add multiple masks at once by pressing the plus icon. Once you have the mask(s) or property selected and adjusted, click the Ok button or hit enter.

![Layer Mask list](https://i.imgur.com/pQdktj8.png)
![Layer Property options](https://i.imgur.com/th1ov0E.png)

### Multiframe Select Stroke From Active
Multiframe Select Stroke from Active copies the selection state of strokes in the active frame to the strokes of other frames that are selected while in multiframe mode. It matches strokes between frames by their order, so if the stroke order is changed then it won't select the correct strokes in the frames that have the order changed.

![Multiframe Select Stroke From Active](https://i.imgur.com/Gi2or1e.gif)
