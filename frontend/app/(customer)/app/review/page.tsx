"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { ChevronLeft, Camera, Star } from "lucide-react";
import { cn } from "@/lib/utils";

export default function ReviewPage() {
  const router = useRouter();
  const [rating, setRating] = useState(0);
  const [feedback, setFeedback] = useState("");
  const [submitted, setSubmitted] = useState(false);

  if (submitted) {
    return (
      <div className="animate-fade-in flex flex-col items-center justify-center min-h-[70vh] px-6 text-center">
        <div className="text-5xl mb-4">🎉</div>
        <h2 className="text-xl font-bold text-text-primary mb-2">Thank you!</h2>
        <p className="text-text-secondary mb-6">Your feedback helps us serve you better.</p>
        <button onClick={() => router.push("/app")} className="bg-primary-600 text-white font-semibold px-8 py-3 rounded-2xl">
          Back to Home
        </button>
      </div>
    );
  }

  return (
    <div className="animate-fade-in">
      {/* Header */}
      <div className="px-4 pt-4 pb-3 flex items-center gap-3">
        <button onClick={() => router.back()} className="w-9 h-9 rounded-xl bg-white border border-border flex items-center justify-center">
          <ChevronLeft className="w-5 h-5 text-text-primary" />
        </button>
        <h1 className="text-lg font-bold text-text-primary">Rate & Review</h1>
      </div>

      <div className="px-4">
        {/* Rating */}
        <div className="bg-white border border-border rounded-2xl p-6 text-center">
          <h2 className="text-xl font-bold text-text-primary mb-2">Rate Your Experience</h2>
          <p className="text-sm text-text-muted mb-5">How was your delivery?</p>

          <div className="flex items-center justify-center gap-2 mb-6">
            {[1, 2, 3, 4, 5].map((star) => (
              <button
                key={star}
                onClick={() => setRating(star)}
                className="transition-transform hover:scale-110 active:scale-95"
              >
                <Star
                  className={cn(
                    "w-10 h-10 transition-colors",
                    star <= rating
                      ? "text-yellow-400 fill-yellow-400"
                      : "text-gray-200"
                  )}
                />
              </button>
            ))}
          </div>

          {rating > 0 && (
            <p className="text-sm font-medium text-primary-600 mb-2">
              {rating === 5 ? "Excellent!" : rating === 4 ? "Great!" : rating === 3 ? "Good" : rating === 2 ? "Fair" : "Poor"}
            </p>
          )}
        </div>

        {/* Written Feedback */}
        <div className="mt-4">
          <label className="block text-sm font-medium text-text-primary mb-2">Write your feedback</label>
          <textarea
            value={feedback}
            onChange={(e) => setFeedback(e.target.value)}
            placeholder="Tell us about your experience..."
            rows={4}
            className="w-full border border-border rounded-xl px-4 py-3 text-sm text-text-primary placeholder:text-text-muted focus:outline-none focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500 resize-none transition-all"
          />
        </div>

        {/* Add Photo */}
        <button className="mt-3 flex items-center gap-2 text-primary-600 font-medium text-sm py-2">
          <Camera className="w-5 h-5" /> Add Photo
        </button>

        {/* Submit */}
        <button
          onClick={() => setSubmitted(true)}
          disabled={rating === 0}
          className={cn(
            "w-full mt-6 mb-6 py-4 rounded-2xl font-semibold text-white transition-all",
            rating > 0
              ? "bg-primary-600 hover:bg-primary-700 shadow-lg shadow-primary-600/30"
              : "bg-gray-300 cursor-not-allowed"
          )}
        >
          Submit
        </button>
      </div>
    </div>
  );
}
