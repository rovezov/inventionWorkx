// src/pages/Home.js

import React, { useState } from 'react';
import ProjectList from '../components/Project/ProjectList';
import ProjectForm from '../components/Project/ProjectForm';
import JoinProjectForm from '../components/Project/JoinProjectForm';
import './Home.css';

function Home() {
  const [refresh, setRefresh] = useState(false);

  const refreshProjects = () => setRefresh(!refresh); // Toggle to trigger refresh

  return (
    <div>
      <h1>Welcome to the HaaS System</h1>

      {/* Section for creating a new project */}
      <div className="section project-form">
        <ProjectForm onProjectCreate={refreshProjects} />
      </div>

      {/* Section for joining an existing project by ID */}
      <div className="section join-project">
        <h2>Join a Project</h2>
        <JoinProjectForm />
      </div>

      {/* Section for listing the user's projects */}
      <div className="section project-list">
        <ProjectList refresh={refresh} />
      </div>
    </div>
  );
}

export default Home;
