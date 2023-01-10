const firstImageInput = document.getElementById("FirstImageInput");
const secondImageInput = document.getElementById("SecondImageInput");

const firstImage = document.getElementById("FirstImage");
const secondImage = document.getElementById("SecondImage");
const mixedImage = document.getElementById("MixedImage");

const firstRadios = document.getElementsByName("FirstImageTools");
const secondRadios = document.getElementsByName("SecondImageTools");

const image1Container = document.getElementById("img1cont");
const image2Container = document.getElementById("img2cont");

const checkBox = document.getElementById("checkbox");

const image1MagPath = "../static/images/image1_mag.png?";
const image1PhasePath = "../static/images/image1_phase.png?";

const image2MagPath = "../static/images/image2_mag.png?";
const image2PhasePath = "../static/images/image2_phase.png?";

const imageMixedPath = "../static/images/image_mix.png?";

let cropDimensions = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 1], [0]];

firstImageInput.addEventListener("change", function () {
  let reader = new FileReader();
  reader.onload = () => {
    firstRadios[0].checked = true;
    firstImage.src = reader.result;
    makeCropper(0, image1Container, image1MagPath);
  };
  reader.readAsDataURL(this.files[0]);
  LoadImage(this.files[0], 1)
});

secondImageInput.addEventListener("change", function () {
  let reader = new FileReader();
  reader.onload = () => {
    secondRadios[1].checked = true;
    secondImage.src = reader.result;
    makeCropper(1, image2Container, image2PhasePath);
  };
  reader.readAsDataURL(this.files[0]);
  LoadImage(this.files[0], 2)
}
);

checkBox.addEventListener("change", () => {
  cropDimensions[3] = checkBox.checked ? 1 : 0;
})

for (radio in firstRadios) {
  firstRadios[radio].onclick = function () {
    if (this.value == "Magnitude") {
      cropDimensions[2][0] = 0;
      makeCropper(0, image1Container, image1MagPath);
    }
    else if (this.value == "Phase") {
      cropDimensions[2][0] = 1;
      makeCropper(0, image1Container, image1PhasePath);
    }
  }
}

for (radio in secondRadios) {
  secondRadios[radio].onclick = function () {
    if (this.value == "Magnitude") {
      cropDimensions[2][1] = 0;
      makeCropper(1, image2Container, image2MagPath);
    }
    else if (this.value == "Phase") {
      cropDimensions[2][1] = 1;
      makeCropper(0, image2Container, image2PhasePath);
    }
  }
}

function makeCropper(index, container, imageSrc) {
  let img = document.createElement("img");
  img.id = "image";
  img.src = imageSrc + new Date().getTime();
  container.innerHTML = "";
  container.appendChild(img);
  cropper = new Cropper(img, {
    guides: false,
    autoCrop: false,
    crop(event) {
      cropDimensions[index] = [Math.round(event.detail.x), Math.round(event.detail.y), Math.round(event.detail.width), Math.round(event.detail.height)];
    },
    cropend(event) {
      loadDimensions();
    }
  });
}

function LoadImage(image, index) {
  const xhttp = new XMLHttpRequest();
  xhttp.onload = function () {
    console.log(this.responseText);
  }
  xhttp.open("POST", "/image/" + index, true);
  xhttp.send(image);
}

function loadDimensions() {
  const xhttp = new XMLHttpRequest();
  xhttp.onload = function () {
    console.log(this.responseText);
    mixedImage.src = imageMixedPath + new Date().getTime();
  }
  xhttp.open("POST", "/dimensions", true);
  xhttp.send(cropDimensions);
}
