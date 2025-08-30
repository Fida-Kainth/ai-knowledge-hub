import React, { useEffect, useState } from "react";
import api from "../utils/api";
import { getToken } from "../utils/auth";
import Loader from "../components/Loader";

const Dashboard = () => {
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await api.get("/auth/profile/", {
          headers: { Authorization: `Bearer ${getToken()}` },
        });
        setProfile(res.data);
      } catch {
        setProfile({ error: "Unable to load profile" });
      }
    };
    fetchProfile();
  }, []);

  if (!profile) return <Loader />;

  return (
    <div className="page dashboard">
      <h2>Dashboard</h2>
      {profile.error ? (
        <p className="error">{profile.error}</p>
      ) : (
        <div className="profile-card">
          <p><strong>Username:</strong> {profile.username}</p>
          <p><strong>Email:</strong> {profile.email}</p>
          <p><strong>Joined:</strong> {new Date(profile.date_joined).toLocaleDateString()}</p>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
