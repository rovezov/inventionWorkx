// src/components/Project/ProjectList.js

import React, { useEffect, useState } from 'react';
import { listProjects } from '../../api/projectService';
import { listHardware } from '../../api/hardwareService';
import HardwareCheckoutForm from '../Hardware/HardwareCheckoutForm';
import HardwareCheckinForm from '../Hardware/HardwareCheckinForm';

function ProjectList({ refresh }) {
  const [projects, setProjects] = useState([]);
  const [globalHardware, setGlobalHardware] = useState([]);
  const [error, setError] = useState('');

  // Function to refresh both project and global hardware data
  const refreshAllData = async () => {
    try {
      const userid = localStorage.getItem('userid');
      const projectData = await listProjects(userid);
      const hardwareData = await listHardware();

      setProjects(projectData);
      setGlobalHardware(hardwareData);
    } catch (err) {
      setError(err.message || "Failed to load data");
    }
  };

  useEffect(() => {
    refreshAllData(); // Load data initially
  }, [refresh]); // Trigger data refresh when `refresh` changes

  return (
    <div>
      <h2>Your Projects</h2>
      {error && <p>{error}</p>}

      {/* Display Global Resources */}
      <div className="section global-resources">
        <h3>Global Hardware Resources</h3>
        <ul>
          {globalHardware.map((item, index) => (
            <li key={index}>
              <strong>{item.hardware_name}</strong>: {item.availability} available / {item.capacity} total
            </li>
          ))}
        </ul>
      </div>

      {/* List of Projects */}
      <ul>
        {projects.map((project) => (
          <li key={project.id}>
            <h3>{project.name}</h3>
            <p>{project.description}</p>
            
            {/* Display only if hardware is checked out */}
            {project.hardware && project.hardware.length > 0 ? (
              <>
                <h4>Checked-Out Hardware:</h4>
                <ul>
                  {project.hardware.map((hw, index) => (
                    <li key={index}>
                      {hw.name}: {hw.quantity} units
                    </li>
                  ))}
                </ul>
              </>
            ) : (
              <p>No hardware checked out.</p>
            )}

            {/* Checkout and Check-In Forms */}
            <HardwareCheckoutForm 
              projectId={project.id} 
              globalHardware={globalHardware} 
              onActionComplete={refreshAllData} 
            />
            <HardwareCheckinForm 
              projectId={project.id} 
              projectHardware={project.hardware} 
              onActionComplete={refreshAllData} 
            />
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ProjectList;
