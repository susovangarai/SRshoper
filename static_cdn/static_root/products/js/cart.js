var cartBtns = document.getElementsByClassName("update-cart");
for (var i = 0; i < cartBtns.length; i++) {
  cartBtns[i].addEventListener("click", function () {
    var productId = this.dataset.product;
    var action = this.dataset.action;

    console.log("productId:", productId, "Action:", action);
    console.log("User:", user);

    if (user != "AnonymousUser") {
      updateUserOrder(productId, action);
    }
  });
}

function updateUserOrder(productId, action) {
  var url = "/cart/update/";

  fetch(url, {
    method: "POST",
    headers: {
      "Content-type": "application/JSON",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ productId: productId, action: action }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      location.reload();
    });
}
