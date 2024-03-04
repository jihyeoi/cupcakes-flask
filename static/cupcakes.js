"use strict";

const $cupcakeList = $("#cupcake_list");
const $cupcakeForm = $("#cupcake_form");
const $flavorInput = $("#flavor");
const $ratingInput = $("#rating");
const $sizeInput = $("#size");
const $imageUrlInput = $("#image_url");

const BASE_URL = "http://127.0.0.1:5000";

/** Makes request to API, returns list of all cupcakes */
async function getCupcakeList() {
  const response = await fetch(`${BASE_URL}/api/cupcakes`);
  const responseObj = await response.json();

  return responseObj["cupcakes"];
}

/** Takes in list of cupcakes, creates UI elements for each cupcake,
 * and adds elements to the page */
function updateCupcakeListUi(cupcakes) {
  for (let cupcake of cupcakes) {
    addCupcakeToUi(cupcake);
  }
}

/** Gets cupcakes and adds them to the UI */
async function getCupcakesAndUpdateUi() {
  const cupcakes = await getCupcakeList();
  updateCupcakeListUi(cupcakes);
}

function addCupcakeToUi(cupcake) {
  const $cupcake = $(`<li>${cupcake.flavor} is a ${cupcake.size} and is rated
                    ${cupcake.rating}. Here is a photo: <img src='${cupcake.image_url}'</li>`);

  $cupcakeList.append($cupcake);
}


async function handleFormSubmit(evt) {
  evt.preventDefault();

  const form_inputs = {
    flavor: $flavorInput.val(),
    rating: $ratingInput.val(),
    image_url: $imageUrlInput.val(),
    size: $sizeInput.val()
  };

  const new_cupcake = await addNewCupcakeRequest(form_inputs);
  addCupcakeToUi(new_cupcake);
  $cupcakeForm.trigger('reset');
}


async function addNewCupcakeRequest(form_inputs) {
  const response = await fetch(`${BASE_URL}/api/cupcakes`, {
    method: "POST",
    body: JSON.stringify(form_inputs),
    headers: {
      "Content-Type": "application/json"
    }
  });
  const responseObj = await response.json();

  return responseObj["cupcake"];
}


$cupcakeForm.on('submit', handleFormSubmit);
getCupcakesAndUpdateUi();


