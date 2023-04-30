import React, { useState, useEffect } from 'react';
import './style.css';
import axios from 'axios';

const LeadCRUD = () => {
  const [leads, setLeads] = useState([    { id: 1, name: 'John Doe', email: 'john@example.com', phone: '555-1234' },    { id: 2, name: 'Jane Smith', email: 'jane@example.com', phone: '555-5678' },    { id: 3, name: 'Bob Johnson', email: 'bob@example.com', phone: '555-9012' },  ]);
  const [newLead, setNewLead] = useState({ name: '', email: '', phone: '' });
  const [editLead, setEditLead] = useState(null);
  const [showModal, setShowModal] = useState(false);

  const userId = localStorage.getItem('userId');
/*
useEffect(() => {
    const fetchLeads = async () => {
      try {
        const res = await axios.get(`http://localhost:8080/api/leads/${userId}/leads`);
        setLeads(res.data.data);
      } catch (error) {
        console.log(error);
      }
    };

    fetchLeads();
  }, [userId]);*/

  const handleChange = (event) => {
    setNewLead({ ...newLead, [event.target.name]: event.target.value });
  };

  const handleAddLead = async () => {
    console.log("Hello");
    //setLeads([...leads, { ...newLead, id: Math.max(...leads.map((l) => l.id)) + 1 }]);
    //setNewLead({ name: '', email: '', phone: '' });

    try {
      const res = await axios.post(`http://localhost:8080/api/leads/${userId}/leads`, newLead);
      setLeads([...leads, res.data.data]);
      setNewLead({ name: '', email: '', phone: '' });
    } catch (error) {
      console.log(error);
    }

  };


  const handleDeleteLead = async (lead) => {
    //setLeads(leads.filter((l) => l !== lead));

    try {
      await axios.delete(`http://localhost:8080/api/leads/${userId}/leads/${lead._id}`);
      setLeads(leads.filter((l) => l !== lead));
    } catch (error) {
      console.log(error);
    }

  };

  const handleEditLead = (lead) => {
    setEditLead(lead);
    setNewLead(lead);
    setShowModal(true);
  };

  const handleUpdateLead = async () => {

    try {
      const res = await axios.put(`http://localhost:8080/api/leads/${userId}/leads/${editLead._id}`, newLead);
      const updatedLeads = leads.map((l) => (l === editLead ? res.data.data : l));
      setLeads(updatedLeads);
      setNewLead({ name: '', email: '', phone: '' });
      setEditLead(null);
      setShowModal(false);
    } catch (error) {
      console.log(error);
    }

  };

  const handleAddLeadModal = () => {
    setShowModal(true);
  };

  return (
    <div className='container'>
      <h2>Leads</h2>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Phone</th>
            <th></th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {leads && leads.map((lead) => (
            <tr key={lead.id}>
              <td>{lead.name}</td>
              <td>{lead.email}</td>
              <td>{lead.phone}</td>
              <td>
                <button onClick={() => handleEditLead(lead)}>Edit</button>
              </td>
              <td>
                <button onClick={() => handleDeleteLead(lead)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <button onClick={handleAddLeadModal}>Add Lead</button>
      {showModal && (
        <div className='modal' style={{ display: showModal ? 'block' : 'none' }}>
        <div className='modal-content'>
          <span className='close' onClick={() => setShowModal(false)}>&times;</span>
          <h2>{editLead ? 'Edit Lead' : 'Add Lead'}</h2>
          <form>
            <label >
              Name:
              <input type="text" name="name" value={newLead.name} onChange={handleChange} />
            </label>
            <label>
              Email:
              <input type="text" name="email" value={newLead.email} onChange={handleChange} />
            </label>
            <label>
              Phone:
              <input type="text" name="phone" value={newLead.phone} onChange={handleChange} />
            </label>
            {editLead ? (
              <button type="button" onClick={handleUpdateLead}>
                Update Lead
              </button>
            ) : (
              <button type="button" onClick={handleAddLead}>
                Add Lead
              </button>
            )}
          </form>
        </div>
      </div> )}
    </div>);

}

export default LeadCRUD;