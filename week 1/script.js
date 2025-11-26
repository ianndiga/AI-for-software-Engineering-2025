const courses = [
  { id: 1, title: "HTML & CSS Basics", description: "Learn the building blocks of the web." },
  { id: 2, title: "JavaScript Essentials", description: "Make your websites interactive." },
  { id: 3, title: "Python for Beginners", description: "Start coding with Python." }
];

const loggedInUser = localStorage.getItem("loggedInUser");
if (!loggedInUser) {
  window.location.href = "login.html";
}

document.getElementById("welcome-user").innerText = `Hello, ${loggedInUser}!`;

const courseList = document.getElementById("course-list");
const progressBar = document.getElementById("progress-bar");

const userProgressKey = `completedCourses_${loggedInUser}`;
const completedCourses = JSON.parse(localStorage.getItem(userProgressKey)) || [];

function renderCourses() {
  courseList.innerHTML = '';
  courses.forEach(course => {
    const div = document.createElement('div');
    div.className = 'card p-3 shadow-sm';
    div.style.width = '18rem';
    div.innerHTML = `
      <h5>${course.title}</h5>
      <p>${course.description}</p>
      <button class="btn ${completedCourses.includes(course.id) ? 'btn-success' : 'btn-primary'}" onclick="toggleComplete(${course.id})">
        ${completedCourses.includes(course.id) ? 'Completed' : 'Mark as Completed'}
      </button>
    `;
    courseList.appendChild(div);
  });
  updateProgress();
}

function toggleComplete(id) {
  const index = completedCourses.indexOf(id);
  if (index > -1) completedCourses.splice(index, 1);
  else completedCourses.push(id);

  localStorage.setItem(userProgressKey, JSON.stringify(completedCourses));
  renderCourses();
}

function updateProgress() {
  const percent = Math.round((completedCourses.length / courses.length) * 100);
  progressBar.style.width = `${percent}%`;
  progressBar.innerText = `${percent}% Completed`;
}

function logout() {
  localStorage.removeItem("loggedInUser");
  window.location.href = "login.html";
}

renderCourses();

function logout() {
  localStorage.removeItem("loggedInUser");
  window.location.href = "login.html";
}
