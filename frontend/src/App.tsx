import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Layout from './components/Layout';
import ErrorBoundary from './components/ErrorBoundary';

import Dashboard from './pages/Dashboard';
import Vehicles from './pages/Vehicles';
import Drivers from './pages/Drivers';
import Trips from './pages/Trips';
import Maintenance from './pages/Maintenance';
import Expenses from './pages/Expenses';
import Analytics from './pages/Analytics';
import TrackingPage from './pages/TrackingPage';
import NotFoundFallback from './pages/NotFoundFallback';

const MANAGEMENT_ROLES = ['Fleet Manager', 'Dispatcher', 'Safety Officer', 'Financial Analyst'];

const PrivateRoute = ({ children, allowedRoles }: { children: React.ReactNode, allowedRoles?: string[] }) => {
  const token = localStorage.getItem('token');
  const role = localStorage.getItem('role');

  if (!token) {
    return <Navigate to="/login" />;
  }

  if (allowedRoles && role && !allowedRoles.includes(role)) {
    // Customer gets redirected to tracking, others to dashboard
    if (role === 'Customer') {
      return <Navigate to="/tracking" />;
    }
    return <Navigate to="/dashboard" />;
  }

  return <Layout role={role}>{children}</Layout>;
};

const App: React.FC = () => {
  return (
    <ErrorBoundary>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />

          {/* Management routes — not accessible to CUSTOMER */}
          <Route path="/" element={<PrivateRoute allowedRoles={MANAGEMENT_ROLES}><Dashboard /></PrivateRoute>} />
          <Route path="/dashboard" element={<PrivateRoute allowedRoles={MANAGEMENT_ROLES}><Dashboard /></PrivateRoute>} />
          <Route path="/vehicles" element={<PrivateRoute allowedRoles={MANAGEMENT_ROLES}><Vehicles /></PrivateRoute>} />
          <Route path="/drivers" element={<PrivateRoute allowedRoles={MANAGEMENT_ROLES}><Drivers /></PrivateRoute>} />
          <Route path="/trips" element={<PrivateRoute allowedRoles={MANAGEMENT_ROLES}><Trips /></PrivateRoute>} />
          <Route path="/maintenance" element={<PrivateRoute allowedRoles={MANAGEMENT_ROLES}><Maintenance /></PrivateRoute>} />
          <Route path="/expenses" element={<PrivateRoute allowedRoles={['Fleet Manager', 'Financial Analyst']}><Expenses /></PrivateRoute>} />
          <Route path="/analytics" element={<PrivateRoute allowedRoles={['Fleet Manager', 'Financial Analyst']}><Analytics /></PrivateRoute>} />

          {/* Customer tracking route — accessible to all authenticated users */}
          <Route path="/tracking" element={<PrivateRoute><TrackingPage /></PrivateRoute>} />

          {/* 404 fallback */}
          <Route path="*" element={<NotFoundFallback />} />
        </Routes>
      </Router>
    </ErrorBoundary>
  );
};

export default App;
