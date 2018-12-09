let img;
let drawingRect = false;
let rectCorner1;
let rectCorner2;

// let xmin_prev = -2;
// let ymin_prev = -1.5;
// let xmax_prev = 2;
// let ymax_prev = 1.5;

let limits = [
	[-2, -1.5, 2, 1.5]
];

// let xmin = -2;
// let ymin = -1.5;
// let xmax = 2;
// let ymax = 1.5;

let img_width = 400;
let img_height = 300;

function success(response) {
	img.loadPixels();
	for (var i = img.pixels.length - 1; i >= 0; i--) {
		img.pixels[i] = response.img[i];
	}
	img.updatePixels();
}

function failure(response) {
}

function resetZoom() {
	limits = [
		[-2, -1.5, 2, 1.5]
	];
	makeRequest();
}

function prevZoom() {
	if (limits.length > 1) {
		limits.pop()
		makeRequest();
	}
}

function setup() {
	c = createCanvas(img_width, img_height).parent('canvasHolder');

	img = createImage(img_width, img_height);
	rectCorner1 = createVector(0, 0);
	rectCorner2 = createVector(0, 0);

	prev = createButton('Zoom out').parent('fields');
	prev.mousePressed(prevZoom);

	reset = createButton('Reset zoom').parent('fields');
	reset.mousePressed(resetZoom);

	makeRequest();

	rectMode(CORNERS)
}

function draw() {
	background(51);
	image(img, 0, 0);

	noFill();
	strokeWeight(2);
	stroke(200);
	if (drawingRect) {
		rect(rectCorner1.x, rectCorner1.y, mouseX, mouseY);
	}
}

function makeRequest() {
	let data = {
		limits: limits[limits.length - 1],
		img_width: img_width,
		img_height: img_height
	}
	httpPost('api', 'json', data, success, failure);
}

function mousePressed() {
	if (mouseX > img_width || mouseX < 0 || mouseY > img_height || mouseY < 0) {
		return;
	}
	if (drawingRect) {
		rectCorner2 = createVector(mouseX, mouseY);

		let h = rectCorner2.y - rectCorner1.y;
		let w = rectCorner2.x - rectCorner1.x;

		h = Math.sign(h) * abs(w) * img_height / img_width;
		rectCorner2.y = rectCorner1.y + h;

		let limits_recent = limits[limits.length - 1];
		let xmin = limits_recent[0]
		let ymin = limits_recent[1]
		let xmax = limits_recent[2]
		let ymax = limits_recent[3]

		let xmin_new = map(rectCorner1.x, 0, img_width, xmin, xmax)
		let ymin_new = map(rectCorner1.y, 0, img_height, ymin, ymax)
		let xmax_new = map(rectCorner2.x, 0, img_width, xmin, xmax)
		let ymax_new = map(rectCorner2.y, 0, img_height, ymin, ymax)

		limits.push([xmin_new, ymin_new, xmax_new, ymax_new]);

		drawingRect = false;
		makeRequest();
	} else {
		rectCorner1 = createVector(mouseX, mouseY);
		drawingRect = true;
	}
}