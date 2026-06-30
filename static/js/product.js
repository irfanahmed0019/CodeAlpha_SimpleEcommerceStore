console.log("product.js loaded");
const mainImage = document.getElementById("main-product-image");
console.log(mainImage);
const thumbnails=document.querySelectorAll(".thumbnail");

thumbnails.forEach((thumbnail)=>{
    thumbnail.addEventListener("click",()=>{
        mainImage.src=thumbnail.dataset.image;
    });
});

