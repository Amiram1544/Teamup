/*function showTab(tabName) {
    const sections = document.querySelectorAll('.tab-section');
    sections.forEach(section => section.style.display = 'none');

    document.getElementById(tabName).style.display = 'block';
}*/

function openTaskModal() {
    
    const topic = document.getElementById("task-topic").value.trim()

    if (!topic) {
        alert("You must Enter a topic first.")
        return
    }

    document.getElementById("task-modal").style.display = "flex";
}

function closeTaskModal(){

    document.getElementById("task-modal").style.display = "none";

    document.getElementById("task-notes").value = '';
    document.getElementById("task-description").value = '';
}