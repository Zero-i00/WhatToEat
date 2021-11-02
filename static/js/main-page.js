const searchBtn = document.querySelector('.search-btn')
const cancelBtn = document.querySelector('.cancel-btn')
const searchBox = document.querySelector('.search-box')
const searchInput = document.getElementById('generate_btn')
const titleActivateInput = document.getElementById('el-id')




searchBtn.onclick = () => {
    searchBox.classList.add('active');
    searchInput.classList.add('active');
    searchBtn.classList.add('active');
    cancelBtn.classList.add('active');

}

titleActivateInput.onclick = () => {
    searchBox.classList.add('active');
    searchInput.classList.add('active');
    searchBtn.classList.add('active');
    cancelBtn.classList.add('active');
}

searchInput.onclick = () => {
    searchBox.classList.remove('active');
    searchInput.classList.remove('active');
    searchBtn.classList.remove('active');
    cancelBtn.classList.remove('active');

    searchInput.setAttribute('type', 'submit')
}


cancelBtn.onclick = () => {
    searchBox.classList.remove('active');
    searchInput.classList.remove('active');
    searchBtn.classList.remove('active');
    cancelBtn.classList.remove('active');
}
