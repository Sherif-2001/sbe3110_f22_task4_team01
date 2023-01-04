const FirstImageInput = document.getElementById("FirstImageInput");
const SecondImageInput = document.getElementById("SecondImageInput");

const FirstImage = document.getElementById("FirstImage");
const SecondImage = document.getElementById("SecondImage");
const MixedImage = document.getElementById("MixedImage");

const FirstTools = document.getElementsByName("FirstImageTools");
const SecondTools = document.getElementsByName("SecondImageTools");

const img1cont = document.getElementById("img1cont");
const img2cont = document.getElementById("img2cont");

const checkBox = document.getElementById("checkbox");

const image1Path = "../static/images/image1.png";
const image1MagPath = "../static/images/image1_mag.png?";
const image1PhasePath = "../static/images/image1_phase.png?";

const image2Path = "../static/images/image2.png";
const image2MagPath = "../static/images/image2_mag.png?";
const image2PhasePath = "../static/images/image2_phase.png?";

const imageMixed = "../static/images/image_mix.png?";

let cropDimensions = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0], [0]];

FirstImageInput.addEventListener("change", function () {
  let reader = new FileReader();
  reader.onload = e => {
    if (e.target.result) {
      setTimeout(function () {
        FirstTools[0].checked = true;
        FirstImage.src = e.target.result;
        let img = document.createElement("img");
        img.id = "image";
        img.src = image1MagPath + new Date().getTime();
        img1cont.innerHTML = "";
        img1cont.appendChild(img);
        cropper = new Cropper(img, {
          crop(event) {
            cropDimensions[0] = [Math.round(event.detail.x), Math.round(event.detail.y), Math.round(event.detail.width), Math.round(event.detail.height)];
            loadDimensions();
          }
        });
      }, 1000);
    }
  };
  reader.readAsDataURL(this.files[0]);
  LoadImage(this.files[0], 1);
});

SecondImageInput.addEventListener("change", function () {
  let reader = new FileReader();
  reader.onload = e => {
    if (e.target.result) {
      setTimeout(() => {
        SecondTools[1].checked = true;
        SecondImage.src = e.target.result;
        let img = document.createElement("img");
        img.id = "image";
        img.src = image2PhasePath + new Date().getTime();
        img2cont.innerHTML = "";
        img2cont.appendChild(img);
        cropper2 = new Cropper(img, {
          crop(event) {
            cropDimensions[1] = [Math.round(event.detail.x), Math.round(event.detail.y), Math.round(event.detail.width), Math.round(event.detail.height)];
            loadDimensions();
          }
        });
      }, 1000);

    }
  };
  reader.readAsDataURL(this.files[0]);
  LoadImage(this.files[0], 2);
});

checkBox.addEventListener("change", function () {
  cropDimensions[3] = this.checked ? 1 : 0;
  loadDimensions();
})

for (radio in FirstTools) {
  FirstTools[radio].onclick = function () {
    if (this.value == "Magnitude") {
      cropDimensions[2][0] = 0;
      let img = document.createElement("img");
      img.id = "image";
      img.src = image1MagPath + new Date().getTime();
      img1cont.innerHTML = "";
      img1cont.appendChild(img);
      cropper = new Cropper(img, {
        crop(event) {
          cropDimensions[0] = [Math.round(event.detail.x), Math.round(event.detail.y), Math.round(event.detail.width), Math.round(event.detail.height)];
          loadDimensions();
        }
      });
    } else if (this.value == "Phase") {
      cropDimensions[2][0] = 1;
      let img = document.createElement("img");
      img.id = "image";
      img.src = image1PhasePath + new Date().getTime();
      img1cont.innerHTML = "";
      img1cont.appendChild(img);
      cropper = new Cropper(img, {
        crop(event) {
          cropDimensions[0] = [Math.round(event.detail.x), Math.round(event.detail.y), Math.round(event.detail.width), Math.round(event.detail.height)];
          loadDimensions();
        }
      });
    }
  }
}

for (radio in SecondTools) {

  SecondTools[radio].onclick = function () {
    if (this.value == "Magnitude") {
      cropDimensions[2][1] = 0;
      let img = document.createElement("img");
      img.id = "image";
      img.src = image2MagPath + new Date().getTime();
      img2cont.innerHTML = "";
      img2cont.appendChild(img);
      cropper = new Cropper(img, {
        crop(event) {
          cropDimensions[1] = [Math.round(event.detail.x), Math.round(event.detail.y), Math.round(event.detail.width), Math.round(event.detail.height)];
          loadDimensions();
        }
      });
    } else if (this.value == "Phase") {
      cropDimensions[2][1] = 1;
      let img = document.createElement("img");
      img.id = "image";
      img.src = image2PhasePath + new Date().getTime();
      img2cont.innerHTML = "";
      img2cont.appendChild(img);
      cropper = new Cropper(img, {
        crop(event) {
          cropDimensions[1] = [Math.round(event.detail.x), Math.round(event.detail.y), Math.round(event.detail.width), Math.round(event.detail.height)];
          loadDimensions();
        }
      });
    }
  }
}

function LoadImage(data, index) {
  const xhttp = new XMLHttpRequest();
  xhttp.onload = function () {
    console.log(this.responseText);
  }
  if (index == 1) {
    xhttp.open("POST", "/image1", true);
  } else {
    xhttp.open("POST", "/image2", true);
  }
  xhttp.send(data);
}

function loadDimensions() {
  const xhttp = new XMLHttpRequest();
  xhttp.onload = function () {
    console.log(this.responseText);
  }
  xhttp.open("POST", "/dimensions", true);
  xhttp.send(cropDimensions);
}

function setMixed() {
  MixedImage.src = imageMixed + new Date().getTime();
}

window.setInterval(setMixed, 100)

// $.ajax({
//   url: '/dimensions',
//   type: 'POST',
//   contentType: "application/json; charset=utf-8",
//   cache: false,
//   processData: false,
//   async: true,
//   data: JSON.stringify({
//     "dimensions": cropDimensions
//   }),
//   success: function (response) {
//     console.log("Sent Successfuly");
//   }
// });
