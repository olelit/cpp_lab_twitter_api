let go_id = document.querySelector('#go_to_id');

if(go_id){
    go_id.addEventListener("click", (e) => {
        e.preventDefault();
        let id = document.querySelector("#get_id").value;
        window.location.href = "/user/"+id;
    })
}