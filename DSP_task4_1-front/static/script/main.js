let FirstImageInput = document.getElementById("FirstImageInput");
let SecondImageInput = document.getElementById("SecondImageInput");

let FirstImageBtn = document.getElementById("FirstImageBtn");
let SecondImageBtn = document.getElementById("SecondImageBtn");
let MixButton = document.getElementById("MixButton");

let FirstImage = document.getElementById("FirstImage");
let SecondImage = document.getElementById("SecondImage");
let MixedImage = document.getElementById("MixedImage");

let FirstTools = document.getElementsByName("FirstImageTools");
let SecondTools = document.getElementsByName("SecondImageTools");

form = document.getElementById("SubmitForm");

FirstImageInput.addEventListener("change", function () {
  let reader = new FileReader();
  reader.addEventListener("load", () => {
    FirstImage.src = reader.result;
    FirstImage.style.display = "flex";
    FirstTools[0].checked = true;
  });
  reader.readAsDataURL(this.files[0]);
  FirstImageInput.removeEventListener();
});

SecondImageInput.addEventListener("change", function () {
  let reader = new FileReader();
  reader.addEventListener("load", () => {
    SecondImage.src = reader.result;
    SecondImage.style.display = `flex`;
    SecondTools[0].checked = true;
  });
  reader.readAsDataURL(this.files[0]);
}
);

for (radio in FirstTools) {
  FirstTools[radio].onclick = function () {
    if (this.value == "Original") {
      FirstImage.src = "../static/images/image1.png";
    } else if (this.value == "Magnitude") {
      FirstImage.src = "../static/images/image1_mag.png";
    } else if (this.value == "Phase") {
      FirstImage.src = "../static/images/image1_phase.png";
    }
  }
}

for (radio in SecondTools) {
  SecondTools[radio].onclick = function () {
    if (this.value == "Original") {
      SecondImage.src = "../static/images/image2.png";
    } else if (this.value == "Magnitude") {
      SecondImage.src = "../static/images/image2_mag.png";
    } else if (this.value == "Phase") {
      SecondImage.src = "../static/images/image2_phase.png";
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