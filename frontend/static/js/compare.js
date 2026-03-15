let compareList = [];

function addToCompare(productId) {
  if (compareList.length >= 2) {
    alert("Only 2 products allowed");
    return;
  }
  compareList.push(productId);

  localStorage.setItem("compare", JSON.stringify(compareList));

  alert("Product added to compare");
}
