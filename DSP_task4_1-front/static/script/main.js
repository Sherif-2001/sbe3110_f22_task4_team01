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
cropper1 = '';
cropper2 = '';

let firstimagecont = document.getElementById("firstimagecont")
let secondimagecont = document.getElementById("secondimagecont")


let save1 = document.getElementById("saveBtn1");
let save2 = document.getElementById("saveBtn2");

let dwn1 = document.getElementById("download1");
let dwn2 = document.getElementById("download2");


FirstImageInput.addEventListener("change", function () {
  let reader = new FileReader();
  // reader.addEventListener("load", () => {
  // cropper.destroy();
  // FirstImage.src = reader.result;
  // FirstImage.style.display = "flex";
  // FirstTools[0].checked = true;
  // cropper = new Cropper(FirstImage);
  reader.onload = e => {
    if (e.target.result) {
      // create new image
      let img = document.createElement('img');
      img.id = 'image';
      img.src = e.target.result;
      img.style = "  display: flex; max-width: 100%; max-height: 100%; border-radius: 5%; object-fit: contain;";
      // clean result before
      firstimagecont.innerHTML = '';
      // append new image
      firstimagecont.appendChild(img);
      // init cropper
      cropper1 = new Cropper(img);
    }
  };

  // });
  reader.readAsDataURL(this.files[0]);
  FirstImageInput.removeEventListener();
});

SecondImageInput.addEventListener("change", function () {
  let reader = new FileReader();
  // reader.addEventListener("load", () => {
  // SecondImage.src = reader.result;
  // SecondImage.style.display = `flex`;
  // SecondTools[0].checked = true;
  // cropper2 = new Cropper(SecondImage);
  // });
  reader.onload = e => {
    if (e.target.result) {
      // create new image
      let img = document.createElement('img');
      img.id = 'image';
      img.src = e.target.result;
      img.style = "  display: flex; max-width: 100%; max-height: 100%; border-radius: 5%; object-fit: contain;";
      // clean result before
      secondimagecont.innerHTML = '';
      // append new image
      secondimagecont.appendChild(img);
      // init cropper
      cropper2 = new Cropper(img);
    }
  };

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


// save on click
save1.addEventListener('click', e => {
  e.preventDefault();
  // get result to data uri
  let imgSrc = cropper1.getCroppedCanvas({ width: 300 }).toDataURL();
  // remove hide class of img
  FirstImage.classList.remove('hide');
  // img_result.classList.remove('hide');
  // show image FirstImage
  FirstImage.src = imgSrc;
  // dwn.classList.remove('hide');
  dwn.download = 'image1.png';
  dwn.setAttribute('href', imgSrc);
});


save2.addEventListener('click', e => {
  e.preventDefault();
  // get result to data uri
  let imgSrc = cropper2.getCroppedCanvas({ width: 300 }).toDataURL();
  // remove hide class of img
  SecondImage.classList.remove('hide');
  // img_result.classList.remove('hide');
  // show image SecondImage
  SecondImage.src = imgSrc;
  // dwn.classList.remove('hide');
  dwn.download = 'image2.png';
  dwn.setAttribute('href', imgSrc);
});