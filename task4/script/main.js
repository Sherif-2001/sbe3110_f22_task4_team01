let FirstImageInput = document.getElementById("FirstImageInput");
let SecondImageInput = document.getElementById("SecondImageInput");
let FirstImage = document.getElementById("FirstImage");
let FirstImageBtn = document.getElementById("FirstImageBtn");
let SecondImageBtn = document.getElementById("SecondImageBtn");
let SecondImage = document.getElementById("SecondImage");
var path = "";

FirstImageInput.addEventListener("change", function () {
  let reader = new FileReader();
  reader.addEventListener("load", () => {
    FirstImage.src = reader.result;
    FirstImage.style.display = `flex`;
  });
  reader.readAsDataURL(this.files[0]);
  FirstImageInput.removeEventListener();
});

SecondImageInput.addEventListener("change", function (){
  let reader = new FileReader();
  reader.addEventListener("load", () => {
    SecondImage.src = reader.result;
    SecondImage.style.display = `flex`;
  });
  reader.readAsDataURL(this.files[0]);
}
);