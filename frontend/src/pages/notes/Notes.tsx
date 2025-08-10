import React, { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { NotesService } from "@/client/sdk.gen";
import type { Note } from "@/client/types.gen";
import { useNavigate } from "react-router-dom";
import useAuth from "@/hooks/use-auth";
import Navbar from "@/components/layout/Navbar";
import { useToast } from "@/hooks/use-toast";
import Footer from "@/components/home/Footer";

export default function Notes() {
  const navigate = useNavigate();
  const [notes, setNotes] = useState<Note[]>([]);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [loading, setLoading] = useState(false);
  const { user } = useAuth();
  const { toast } = useToast();

  // Redirect if not logged in, and fetch notes if logged in
  useEffect(() => {
    if (!user) {
      navigate("/", { replace: true });
      return;
    }
    NotesService.readNotes()
      .then(setNotes)
      .catch(() => setNotes([]));
  }, [user, navigate]);

  // Create note
  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      if (!user) throw new Error("User not loaded");
      const note = await NotesService.createNote({
        requestBody: { title, content, user_id: user.id },
      });
      setNotes((prev) => [...prev, note]);
      setTitle("");
      setContent("");
    } catch {
      toast({
        variant: "destructive",
        title: "Could not create Note",
        description: "Could not create Note",
      });
    }
    setLoading(false);
  };

  // Delete note
  const handleDelete = async (id: number) => {
    try {
      await NotesService.deleteNote({ noteId: id });
      setNotes((prev) => prev.filter((n) => n.id !== id));
    } catch {
      toast({
        variant: "destructive",
        title: "Could not delete Note",
        description: "Could not delete Note",
      });
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-background">
      <Navbar />
      <main className="min-h-screen flex-1 flex flex-col items-center justify-center px-4">
        <div className="w-full max-w-xl py-10">
          <h1 className="text-3xl font-bold mb-6 text-center">Notes</h1>
          <form onSubmit={handleCreate} className="space-y-4 mb-8">
            <div>
              <Label htmlFor="title">Title</Label>
              <Input
                id="title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                required
              />
            </div>
            <div>
              <Label htmlFor="content">Content</Label>
              <Input
                id="content"
                value={content}
                onChange={(e) => setContent(e.target.value)}
                required
              />
            </div>
            <Button type="submit" disabled={loading} className="w-full">
              {loading ? "Creating..." : "Create Note"}
            </Button>
          </form>
          <ul className="space-y-4">
            {notes.map((note) => (
              <li
                key={note.id}
                className="border p-4 rounded-md flex justify-between items-center bg-background shadow-sm"
              >
                <div>
                  <div className="font-semibold text-lg">{note.title}</div>
                  <div className="text-gray-600">{note.content}</div>
                </div>
                <Button
                  variant="destructive"
                  onClick={() => handleDelete(note.id)}
                >
                  Delete
                </Button>
              </li>
            ))}
          </ul>
        </div>
      </main>
      <Footer />
    </div>
  );
}
