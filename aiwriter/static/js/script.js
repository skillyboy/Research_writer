const menuBtn = document.querySelector(".menu-button");
const sideBar = document.querySelector(".side-menu");



menuBtn.onclick = () =>{
    sideBar.classList.toggle("show");
}




// Search Page Features 
const closeBtn = document.querySelector(".close");
let searchBar = document.querySelector("#searchbar");

searchBar.onkeyup = () =>{
    if(searchBar.value != "" ){
        closeBtn.style.display = "block";
    } else{
        closeBtn.style.display = "none";
    }
}


closeBtn.onclick = () =>{
    searchBar.value = "";
    closeBtn.style.display = "none";
}

