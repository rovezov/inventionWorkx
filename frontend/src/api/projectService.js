// src/api/projectService.js

import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:5000/api/project';

export const createProject = async (userid, name, id, description) => {
  try {
    const token = localStorage.getItem('token');
    const response = await axios.post(`${BASE_URL}/create`, 
      { userid, name, id, description }, 
      { headers: { Authorization: `Bearer ${token}` } });
    return response.data;
  } catch (error) {
    throw error.response ? error.response.data : new Error("Project creation failed");
  }
};

export const listProjects = async (userid) => {
  try {
    const token = localStorage.getItem('token');
    const response = await axios.get(`${BASE_URL}/list`, {
      headers: { Authorization: `Bearer ${token}` },
      params: { userid }
    });
    return response.data;
  } catch (error) {
    console.error("Error in listProjects:", error);
    throw error.response ? error.response.data : new Error("Failed to retrieve projects");
  }
};

export const joinProject = async (project_id) => {
  try {
    const token = localStorage.getItem('token');
    const userid = localStorage.getItem('userid');
    const response = await axios.post(
      `${BASE_URL}/join`,
      { userid, project_id },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    return response.data;
  } catch (error) {
    throw error.response ? error.response.data : new Error("Join project failed");
  }
};

export const leaveProject = async (project_id) => {
  try {
    const token = localStorage.getItem('token');
    const userid = localStorage.getItem('userid');
    const response = await axios.post(
      `${BASE_URL}/leave`,
      { userid, project_id },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    return response.data;
  } catch (error) {
    throw error.response ? error.response.data : new Error("Leave project failed");
  }
};
