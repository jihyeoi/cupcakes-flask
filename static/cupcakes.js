"use strict";


console.log("File Loaded!");

const $cupcakeList = $("#cupcake_list");

async function getCupcakeList() {

  const base_url = "http://127.0.0.1:5002";

  const response = await fetch(`${base_url}/api/cupcakes`);
  const responseObj = await response.json();

  return responseObj["cupcakes"];

}

function updateCupcakeListUI(cupcakes) {

  for (let cupcake of cupcakes) {
    let $cupcake = $(`<li>${cupcake.flavor} is a ${cupcake.size} and is rated
                    ${cupcake.rating}. Here is a photo: <img src='${cupcake.image_url}'</li>`);

    $cupcakeList.append($cupcake);
  }

}