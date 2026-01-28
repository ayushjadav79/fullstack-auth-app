import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';

const UserList = () => {
    const [users, setUsers] = useState([]);
    const [editingUser, setEditingUser] = useState(null);

    useEffect(() => {
        const token = localStorage.getItem("token"); // Get the token saved during login

        // Fetch the list of users from the backend
        axios.get('http://127.0.0.1:8000/users', {
            headers: {
                Authorization: `Bearer ${token}` // Include the token in the request headers
            }
        })
            .then(response => setUsers(response.data))
            .catch(error => {
                if(error.response?.status === 401) {
                    alert("Not permissible - Please login again");
                }
            });
    }, []);

    const handleDelete = async (id) => {
        if (window.confirm("Are you sure you want to delete this record?")) {
            try {
                await axios.delete(`http://127.0.0.1:8000/users/${id}`);
                // Refresh the list by filtering out the deleted user
                setUsers(users.filter(user => user.id !== id));
            }
            catch (error) {
                console.error("Delete failed", error);
            }
        }
    };

    const handleUpdateSave = async () => {
        try {
            await axios.put(`http://127.0.0.1:8000/users/${editingUser.id}`, editingUser);
            setUsers(users.map(u => u.id === editingUser.id ? editingUser : u));
            setEditingUser(null);
            alert("User updated successfully!");
        }
        catch (error) {
            console.error("Update failed", error);
        }
    };

    return (
        <div className="min-h-screen bg-gray-50 p-8">
            <div className="max-w-6xl mx-auto bg-white shadow-lg rounded-xl p-6">
                <div className="flex justify-between items-center mb-8">
                    <h2 className="text-4xl font-extrabold text-blue-800">Registered Clients</h2>
                    <Link to="/" className="bg-red-500 hover:bg-red-600 text-white px-6 py-2 rounded-lg font-bold transition shadow-md">
                        Logout
                    </Link>
                </div>

                <div className="overflow-x-auto border border-gray-200 rounded-lg">
                    <table className="w-full text-left border-collapse">
                        <thead className="bg-blue-600 text-white">
                            <tr>
                                <th className="p-4 border-b">ID</th>
                                <th className="p-4 border-b">Name</th>
                                <th className="p-4 border-b">Email</th>
                                <th className="p-4 border-b">Gender</th>
                                <th className="p-4 border-b">Hobbies</th>
                                <th className="p-4 border-b">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-200">
                            {users.map((user) => (
                                <tr key={user.id} className="hover:bg-blue-50 transition">
                                    <td className="p-4 font-semibold text-gray-700">{user.id}</td>
                                    <td className="p-4 text-gray-600">{user.first_name} {user.last_name}</td>
                                    <td className="p-4 text-gray-600">{user.email}</td>
                                    <td className="p-4 text-gray-600">{user.gender}</td>
                                    <td className="p-4 text-gray-600">
                                        {user.hobbies?.map(h => (
                                            <span key={h} className="bg-blue-100 text-blue-700 text-xs px-2 py-1 rounded-full mr-1">{h}</span>
                                        ))}
                                    </td>
                                    <td className="p-4 space-x-2">
                                        <button onClick={() => setEditingUser(user)} className="text-blue-600 hover:text-blue-800 font-medium">Edit</button>
                                        <button onClick={() => handleDelete(user.id)} className="text-red-600 hover:text-red-800 font-medium">Delete</button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>

            
            {editingUser && (
                <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
                    <div className="bg-white rounded-2xl shadow-2xl w-full max-w-lg overflow-hidden border border-blue-100">
                        {/* Modal Header */}
                        <div className="bg-blue-600 p-4">
                            <h3 className="text-xl font-bold text-white">Edit User Profile</h3>
                        </div>
                        
                        {/* Modal Body */}
                        <div className="p-6 space-y-4">
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-semibold text-gray-700 mb-1">First Name</label>
                                    <input 
                                        type="text"
                                        value={editingUser.first_name}
                                        className="w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-blue-500 outline-none"
                                        onChange={(e) => setEditingUser({...editingUser, first_name: e.target.value})}
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-semibold text-gray-700 mb-1">Last Name</label>
                                    <input 
                                        type="text"
                                        value={editingUser.last_name}
                                        className="w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-blue-500 outline-none"
                                        onChange={(e) => setEditingUser({...editingUser, last_name: e.target.value})}
                                    />
                                </div>
                            </div>

                            <div>
                                <label className="block text-sm font-semibold text-gray-700 mb-1">Email</label>
                                <input 
                                    type="email"
                                    value={editingUser.email}
                                    className="w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-blue-500 outline-none"
                                    onChange={(e) => setEditingUser({...editingUser, email: e.target.value})}
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-semibold text-gray-700 mb-1">Hobbies (comma separated)</label>
                                <input 
                                    type="text"
                                    value={editingUser.hobbies?.join(", ")}
                                    className="w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-blue-500 outline-none text-blue-700 font-medium"
                                    onChange={(e) => setEditingUser({...editingUser, hobbies: e.target.value.split(",").map(h => h.trim())})}
                                />
                            </div>

                            {/* Modal Footer Buttons */}
                            <div className="flex justify-end space-x-3 pt-4 border-t border-gray-100">
                                <button 
                                    onClick={() => setEditingUser(null)}
                                    className="px-5 py-2 rounded-lg font-semibold text-gray-600 hover:bg-gray-100 transition"
                                >
                                    Cancel
                                </button>
                                <button 
                                    onClick={handleUpdateSave}
                                    className="px-5 py-2 rounded-lg font-bold bg-blue-600 text-white hover:bg-blue-700 shadow-md transition"
                                >
                                    Save Changes
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>      
    );
};

export default UserList;