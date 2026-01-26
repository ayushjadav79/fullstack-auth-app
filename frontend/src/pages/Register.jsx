import React, { useState , useEffect } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';

const Register = () => {
    const [availableHobbies, setAvailableHobbies] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        axios.get('http://127.0.0.1:8000/hobbies')
            .then(response => setAvailableHobbies(response.data))
            .catch(error => console.error("Error fetching hobbies:", error));
    }, []);

    // 1. STATE: This object holds all the form data in "live memory"
    const [formData, setFormData] = useState({
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        dob: '',
        gender: 'Male',
        hobbies: []
    });

    // 2. STATE for the file: Files are handled separately from text
    const [file, setFile] = useState(null);

    // 3. HANDLER: Updates the state every time you type a character
    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    // 4. HANDLER for checkboxes: Updates the hobbies array in state
    const handleCheckboxChange = (e) => {
        const { value, checked } = e.target;
        let updatedHobbies = [...formData.hobbies];

        if (checked) {
            updatedHobbies.push(value);
        }
        else {
            updatedHobbies = updatedHobbies.filter(h => h !== value);
        }

        setFormData({ ...formData, hobbies: updatedHobbies });
    };

    // 5. SUBMIT: The function that talks to the FastAPI backend
    const handleSubmit = async (e) => {
        e.preventDefault();

        const data = new FormData();
        data.append('first_name', formData.first_name);
        data.append('last_name', formData.last_name);
        data.append('email', formData.email);
        data.append('password', formData.password);
        data.append('dob', formData.dob);
        data.append('gender', formData.gender);

        // Convert hobbies array to JSON string before appending
        data.append('hobbies', JSON.stringify(formData.hobbies));
        data.append('file', file);

        try {
            const response = await axios.post('http://127.0.0.1:8000/register', data);
            alert("Registration successful! User ID: " + response.data.id);
            navigate('/users'); // Redirect to user list after successful registration
        }
        catch (error) {
            console.error("Error during registration:", error);
            alert("Registration failed. Check console for details.");
        }
    };

    return (
    <div className="min-h-screen bg-blue-50 flex items-center justify-center p-6">
        <div className="bg-white p-10 rounded-2xl shadow-xl w-full max-w-2xl">
            <h2 className="text-3xl font-extrabold text-blue-600 text-center mb-6">Create Account</h2>
            <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <input name="first_name" placeholder="First Name" onChange={handleChange} className="border p-3 rounded-lg w-full" required />
                <input name="last_name" placeholder="Last Name" onChange={handleChange} className="border p-3 rounded-lg w-full" required />
                <input type="email" name="email" placeholder="Email" onChange={handleChange} className="border p-3 rounded-lg w-full md:col-span-2" required />
                <input type="password" name="password" placeholder="Password" onChange={handleChange} className="border p-3 rounded-lg w-full md:col-span-2" required />
                <input type="date" name="dob" onChange={handleChange} className="border p-3 rounded-lg w-full" required />
                
                <select name="gender" onChange={handleChange} className="border p-3 rounded-lg w-full">
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Other">Other</option>
                </select>

                <div className="md:col-span-2">
                    <label className="block font-bold mb-2 text-gray-700">Hobbies:</label>
                    <div className="flex flex-wrap gap-3">
                        {availableHobbies.map(hobby => (
                            <label key={hobby} className="flex items-center space-x-2 bg-gray-100 px-3 py-1 rounded-md">
                                <input type="checkbox" value={hobby} onChange={handleCheckboxChange} className="accent-blue-600" />
                                <span>{hobby}</span>
                            </label>
                        ))}
                    </div>
                </div>

                <div className="md:col-span-2">
                    <label className="block font-bold mb-1 text-gray-700">Profile Photo:</label>
                    <input type="file" onChange={(e) => setFile(e.target.files[0])} className="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100" required />
                </div>

                <button type="submit" className="md:col-span-2 bg-blue-600 text-white py-3 rounded-xl font-bold hover:bg-blue-700 transition shadow-lg mt-4">
                    Register Now
                </button>
            </form>
            <div className="mt-6 text-center">
                <Link to="/" className="text-blue-600 font-semibold hover:underline">Back to Login</Link>
            </div>
        </div>
    </div>
);
};

export default Register;