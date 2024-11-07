// src/components/Project/JoinProjectForm.js

import React, { useState } from 'react';
import { joinProject } from '../../api/projectService';

function JoinProjectForm() {
  const [projectId, setProjectId] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await joinProject(projectId);
      setSuccess(response.message);  // Show success message
      setError('');  // Clear previous errors
      setProjectId('');  // Reset project ID input
    } catch (err) {
      setError(err.message || 'Failed to join project');  // Show detailed error message from server
      setSuccess('');  // Clear previous success messages
    }
  };

  return (
    <div>
      <h3>Join Project</h3>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {success && <p style={{ color: 'green' }}>{success}</p>}
      <form onSubmit={handleSubmit}>
        <label>Project ID:</label>
        <input
          type="text"
          value={projectId}
          onChange={(e) => setProjectId(e.target.value)}
          required
        />
        <button type="submit">Join</button>
      </form>
    </div>
  );
}

export default JoinProjectForm;
