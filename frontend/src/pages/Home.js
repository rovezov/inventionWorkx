// src/pages/Home.js

import React, { useState } from 'react';
import ProjectList from '../components/Project/ProjectList';
import ProjectForm from '../components/Project/ProjectForm';
import JoinProjectForm from '../components/Project/JoinProjectForm';
import './Home.css';

function Home({ isLoggedIn }) {
  const [refresh, setRefresh] = useState(false);

  const refreshProjects = () => setRefresh(!refresh);

  return (
    <div>
      <h1>Welcome to the HaaS System</h1>

      {isLoggedIn ? (
        <>
          <div className="section project-form">
            <ProjectForm onProjectCreate={refreshProjects} />
          </div>

          <div className="section join-project">
            <h2>Join a Project</h2>
            <JoinProjectForm onProjectJoin={refreshProjects} />
          </div>

          <div className="section project-list">
            <ProjectList refresh={refresh} />
          </div>
        </>
      ) : (
        <p>Please log in to view your projects.</p>
      )}
    </div>
  );
}

export default Home;
