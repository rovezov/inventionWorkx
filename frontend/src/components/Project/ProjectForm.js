// src/components/Project/ProjectForm.js

import React, { useState } from 'react';
import { createProject } from '../../api/projectService';

function ProjectForm({ onProjectCreate }) {
  const [name, setName] = useState('');
  const [id, setId] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const userid = localStorage.getItem('userid'); // Retrieve user ID from localStorage

    try {
      const response = await createProject(userid, name, id, description);
      setSuccess(response.message);  // Display success message
      setError('');  // Clear any previous error
      setName('');
      setId('');
      setDescription('');
      
      // Trigger the refresh callback if provided
      if (onProjectCreate) onProjectCreate();
    } catch (err) {
      setSuccess('');
      setError(err.message || 'Project creation failed');  // Display error message
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Create New Project</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {success && <p style={{ color: 'green' }}>{success}</p>}
      <div>
        <label>Project Name:</label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
      </div>
      <div>
        <label>Project ID:</label>
        <input
          type="text"
          value={id}
          onChange={(e) => setId(e.target.value)}
          required
        />
      </div>
      <div>
        <label>Description:</label>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          required
        />
      </div>
      <button type="submit">Create Project</button>
    </form>
  );
}

export default ProjectForm;
