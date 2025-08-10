import { Link } from "react-router-dom";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/home/Footer";

const Index = () => (
  <div className="min-h-screen flex flex-col bg-background">
    <Navbar />
    <main className="min-h-screen flex-1 flex flex-col items-center justify-center">
      <h1 className="text-4xl font-bold mb-4">Welcome to Notes!</h1>
      <p className="mb-6 text-gray-700">
        A minimal template for FastAPI + React notes app with authentication.
      </p>
      <div className="space-x-4">
        <Link
          to="/auth/login"
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Login
        </Link>
        <Link
          to="/auth/signup"
          className="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300"
        >
          Sign Up
        </Link>
        <Link
          to="/notes"
          className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
        >
          Notes
        </Link>
      </div>
    </main>
    <Footer />
  </div>
);

export default Index;
