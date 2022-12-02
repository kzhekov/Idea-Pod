function showColorPalette(colors: string[]) {
    // Get the canvas element
    const canvas = document.getElementById('canvas') as HTMLCanvasElement;
    const ctx = canvas.getContext('2d') as CanvasRenderingContext2D;

    // Set the width and height of the canvas
    canvas.width = 200;
    canvas.height = 200;

    // Loop through the colors in the palette
    for (let i = 0; i < colors.length; i++) {
        // Set the fill style to the current color
        ctx.fillStyle = colors[i];

        // Draw a rectangle on the canvas with the current color
        ctx.fillRect(i * 50, 0, 50, 200);
    }
}