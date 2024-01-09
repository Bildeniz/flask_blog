function showAlerts(content, type, time){
    const section = document.querySelector('section.container-sm');
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;

    alert.appendChild(document.createTextNode(content));

    section.insertBefore(alert, section.firstChild);

    setTimeout(()=>{
        alert.remove();
    }, time);

}