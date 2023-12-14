function logOut() {
    fetch('/logout/', {
        method: 'DELETE',
    })
        .then(response => response.text()
            .then(res => console.log(res)))
        .catch(err => console.log(err))
};