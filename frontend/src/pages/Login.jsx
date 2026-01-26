import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        const data = new FormData();
        data.append('email', email);
        data.append('password', password);

        try {
            const res = await axios.post('http://127.0.0.1:8000/login', data);
            if (res.data.error) { alert(res.data.error); }
            else { navigate('/users'); }
        }
        catch (err) {
            alert("Login failed");
        }
    };

    return (
        <div className="min-h-screen bg-blue-50 flex items-center justify-center">
            <div className="bg-white p-10 rounded-2xl shadow-xl w-full max-w-md">
                <h2 className="text-3xl font-extrabold text-blue-600 text-center mb-8">Login</h2>
                <form onSubmit={handleLogin} className="space-y-6">
                    <div>
                        <label className="block text-sm font-medium text-gray-700">Email Address</label>
                        <input type="email" placeholder="example@gmail.com" className="mt-1 block w-full px-4 py-3 border border-black rounded-lg focus:ring-blue-500 focus:border-blue-500" 
                                onChange={(e) => setEmail(e.target.value)} required />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700">Password</label>
                        <input type="password" placeholder="••••••••" className="mt-1 block w-full px-4 py-3 border border-black rounded-lg focus:ring-blue-500 focus:border-blue-500" 
                               onChange={(e) => setPassword(e.target.value)} required />
                    </div>
                    <button type="submit" className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition duration-300 shadow-md">
                        Sign In
                    </button>
                </form>
                <div className="mt-8 text-center">
                    <span className="text-gray-600">Don't have an account? </span>
                    <Link to="/register" className="text-blue-600 font-bold hover:underline">Register</Link>
                </div>
            </div>
        </div>
    );
};

export default Login;