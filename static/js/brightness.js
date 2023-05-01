// const sliders = document.querySelectorAll("input[type=range]");

// for (const slider of sliders) {
//   slider.addEventListener('change', (e) => {
//     e.target.nextElementSibling.value = e.target.value;
//   });

//   slider.nextElementSibling.value = slider.value;
// }

function rangeSlide(value) {
  document.getElementById('rangeValue').innerHTML = value;
}