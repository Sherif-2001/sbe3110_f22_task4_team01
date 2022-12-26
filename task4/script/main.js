let FirstImageInput = document.querySelector("#FirstImageInput");
let SecondImageInput = document.querySelector("#SecondImageInput");
let FirstImage = document.querySelector(".FirstImage");
let FirstImageBtn = document.querySelector(".FirstImageBtn");
let SecondImageBtn = document.querySelector(".SecondImageBtn");
let SecondImage = document.querySelector(".SecondImage");
var path = "";

// upload image 
function upload_image_action(image,button) {
  image.style.display = `flex`;
  button.style.display = `none`;
}

FirstImageInput.addEventListener("change", function () {
  let reader = new FileReader();
  FirstImage.style.display = `flex`;
  reader.addEventListener("load", () => {
    path = reader.result;
    FirstImage.src = `${path}`;
    upload_image_action(FirstImage,FirstImageBtn);
  });
  reader.readAsDataURL(this.files[0]);
});

SecondImageInput.addEventListener("change", function () {
  let reader = new FileReader();
  SecondImage.style.display = `flex`;
  reader.addEventListener("load", () => {
    path = reader.result;
    SecondImage.src = `${path}`;
    upload_image_action(SecondImage,SecondImageBtn);
  });
  reader.readAsDataURL(this.files[0]);
});
