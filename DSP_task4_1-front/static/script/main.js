const FirstImageInput = document.getElementById("FirstImageInput");
const SecondImageInput = document.getElementById("SecondImageInput");

const MixButton = document.getElementById("MixButton");

let FirstImageUniform = document.getElementById("FirstImageUniform");
let FirstImageMag = document.getElementById("FirstImageMag");
let FirstImagePhase = document.getElementById("FirstImagePhase");

let SecondImage = document.getElementById("SecondImage");
let MixedImage = document.getElementById("MixedImage");

const FirstTools = document.getElementsByName("FirstImageTools");
const SecondTools = document.getElementsByName("SecondImageTools");

let form = document.getElementById("SubmitForm");

let cropperMag1 = '';
let cropperPhase1 = '';
let cropperMag2 = '';
let cropperPhase2 = '';

let cropDimensions = [];

FirstImageInput.addEventListener("change", function () {
  let reader = new FileReader();
  reader.onload = e => {
    if (e.target.result) {
      FirstImageUniform.src = e.target.result;
      makeCropper(FirstImageMag);
      makeCropper(FirstImagePhase);
    }
  };
  reader.readAsDataURL(this.files[0]);
});

SecondImageInput.addEventListener("change", function () {
  let reader = new FileReader();
  reader.onload = e => {
    if (e.target.result) {
      SecondImageUniform.src = e.target.result;
      makeCropper(SecondImageMag);
      makeCropper(SecondImagePhase);
    }
  };

  reader.readAsDataURL(this.files[0]);
}
);


for (radio in FirstTools) {
  FirstTools[radio].onclick = function () {
    if (this.value == "Uniform") {
      FirstImageUniform.style.display = "flex";
      FirstImageMag.style.display = "none";
      FirstImagePhase.style.display = "none";
    } else if (this.value == "Magnitude") {
      FirstImageMag.src = "../static/images/image1_mag.png";
      FirstImageUniform.style.display = "none";
      FirstImageMag.style.display = "flex";
      FirstImagePhase.style.display = "none";
    } else if (this.value == "Phase") {
      FirstImagePhase.src = "../static/images/image1_phase.png";
      FirstImageUniform.style.display = "none";
      FirstImageMag.style.display = "none";
      FirstImagePhase.style.display = "flex";
    }
  }
}

for (radio in SecondTools) {
  SecondTools[radio].onclick = function () {
    if (this.value == "Uniform") {
      SecondImageUniform.style.display = "flex";
      SecondImageMag.style.display = "none";
      SecondImagePhase.style.display = "none";
    } else if (this.value == "Magnitude") {
      SecondImageMag.src = "../static/images/image2_mag.png";
      SecondImageUniform.style.display = "none";
      SecondImageMag.style.display = "flex";
      SecondImagePhase.style.display = "none";
    } else if (this.value == "Phase") {
      SecondImagePhase.src = "../static/images/image2_phase.png";
      SecondImageUniform.style.display = "none";
      SecondImageMag.style.display = "none";
      SecondImagePhase.style.display = "flex";
    }
  }
}

MixButton.addEventListener("click", function () {
  if (FirstTools[2].checked && SecondTools[2].checked) {
    MixedImage.src = "../static/images/image_mixed_mag2_mag1.png";
  } else if (FirstTools[2].checked && SecondTools[1].checked) {
    MixedImage.src = "../static/images/image_mixed_mag1_p2.png";
  } else if (FirstTools[1].checked && SecondTools[2].checked) {
    MixedImage.src = "../static/images/image_mixed_mag2_p1.png";
  } else if (FirstTools[1].checked && SecondTools[1].checked) {
    MixedImage.src = "../static/images/image_mixed_p1_p2.png";
  } else {
    MixedImage.src = "../static/images/image_mixed_mag2_mag1.png";
  }
});

form.addEventListener('submit', function (event) {
  event.preventDefault();    // prevent page from refreshing
});

function loadDoc() {
  $.ajax({
    url: '/dimensions',
    type: 'POST',
    contentType: "application/json; charset=utf-8",
    cache: false,
    processData: false,
    async: true,
    data: JSON.stringify({
      "dimensions": cropDimensions
    }),
    success: function (response) {
      console.log("Sent Successfuly");
    }
  });
}

function makeCropper(srcHtml) {
  // init cropper
  return Cropper(srcHtml, {
    autoCrop: true,
    autoCropArea: 0.8,
    aspectRatio: 1,
    viewMode: 5,
    crop(event) {
      cropDimensions[0] = [Math.round(event.detail.x), Math.round(event.detail.y), Math.round(event.detail.width), Math.round(event.detail.height)];
      loadDoc();
    },
  });
}