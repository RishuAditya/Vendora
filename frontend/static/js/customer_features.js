function saveRecentlyViewed(productId) {
  let viewed = JSON.parse(localStorage.getItem("recently_viewed")) || [];

  if (!viewed.includes(productId)) {
    viewed.unshift(productId);
  }

  if (viewed.length > 5) {
    viewed.pop();
  }

  localStorage.setItem("recently_viewed", JSON.stringify(viewed));
}

function loadRecentlyViewed() {
  let viewed = JSON.parse(localStorage.getItem("recently_viewed")) || [];

  let section = document.getElementById("recently-viewed-products");

  if (section && viewed.length > 0) {
    fetch("/recent-products?ids=" + viewed.join(","))
      .then((res) => res.json())
      .then((data) => {
        section.innerHTML = "";

        data.forEach((product) => {
          section.innerHTML += `
                <div class="product-card">
                    <h5>${product.name}</h5>
                    <p>₹${product.price}</p>
                </div>
                `;
        });
      });
  }
}
