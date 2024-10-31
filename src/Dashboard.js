import React from 'react';
// import './Dashboard.css';

function Dashboard() {
  return (
    <div className="dashboard-container">
      <h2>Projects</h2>
      <div className="project-options">
        <div className="option-column">
          <h3>Create New Project</h3>
          <button>Create Project</button> {/* Implement project creation logic */}
        </div>
        <div className="option-column">
          <h3>Use Existing Project</h3>
          <button>Open Project</button> {/* Implement logic to open existing projects */}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
