"""
Curated fitness knowledge base.
Each entry is a (topic, question_variants, answer) triple.
question_variants gives the retriever several phrasings to match against,
which improves recall without needing embeddings or an API.
"""

KB = [
    {
        "topic": "Beginner full-body split",
        "q": "beginner workout plan, full body routine, starting out program, new to gym",
        "a": (
            "3-day full-body split (Mon/Wed/Fri), 45-60 min per session:\n"
            "- Squat or leg press: 3x8-10\n"
            "- Bench press or push-up: 3x8-10\n"
            "- Row or lat pulldown: 3x8-10\n"
            "- Romanian deadlift: 2x10\n"
            "- Overhead press: 2x10\n"
            "- Plank: 3x30-45s\n"
            "Rest 60-90s between sets. Add weight when you hit the top of the rep "
            "range with good form on all sets."
        ),
    },
    {
        "topic": "Upper/lower split",
        "q": "4 day split, upper lower program, intermediate routine",
        "a": (
            "4-day upper/lower split:\n"
            "Day 1 Upper: Bench 4x6-8, Row 4x8-10, OHP 3x8-10, Curl/Tricep 3x12\n"
            "Day 2 Lower: Squat 4x6-8, RDL 3x8-10, Leg press 3x10-12, Calf raise 3x15\n"
            "Day 3 rest or light cardio\n"
            "Day 4 Upper (different angles): Incline press, pull-ups, lateral raise\n"
            "Day 5 Lower: Deadlift, lunges, leg curl\n"
            "Progress by adding 2.5-5kg or 1-2 reps per week per lift."
        ),
    },
    {
        "topic": "Push pull legs (PPL)",
        "q": "push pull legs split, 6 day program, advanced routine, bro split",
        "a": (
            "Push/Pull/Legs, run twice a week for 6 days or once for 3:\n"
            "Push: Bench, OHP, incline dumbbell press, tricep pushdown, lateral raise\n"
            "Pull: Deadlift or row, pull-ups, face pulls, bicep curl\n"
            "Legs: Squat, RDL, leg press, leg curl, calf raise\n"
            "3-4 sets of 6-12 reps per exercise. Take one full rest day if running "
            "the 6-day version."
        ),
    },
    {
        "topic": "Short workout, no time",
        "q": "20 minute workout, short on time, quick session, 15 minutes",
        "a": (
            "20-minute dumbbell-only session:\n"
            "- Goblet squat 3x12\n"
            "- Dumbbell row 3x12/side\n"
            "- Push-up 3xAMRAP\n"
            "- Romanian deadlift 3x12\n"
            "- Plank 3x30s\n"
            "Minimal rest (30-45s) between sets to keep it under 20 minutes and "
            "still get a full-body stimulus."
        ),
    },
    {
        "topic": "Bodyweight-only workout",
        "q": "no equipment workout, bodyweight only, home workout, no gym",
        "a": (
            "Bodyweight full-body circuit, 3 rounds:\n"
            "- Push-ups x12-15\n"
            "- Bodyweight squats x20\n"
            "- Walking lunges x10/leg\n"
            "- Pike push-ups or wall handstand hold x8-10 or 20s\n"
            "- Plank x45s\n"
            "- Glute bridges x20\n"
            "Rest 60s between rounds. Add a backpack with books for extra load "
            "once bodyweight gets easy."
        ),
    },
    {
        "topic": "Squat form",
        "q": "how to squat, squat depth, squat form check, knees caving in squat",
        "a": (
            "Squat form checklist:\n"
            "- Feet shoulder-width, toes slightly out\n"
            "- Brace core before descending, chest up\n"
            "- Push knees out in line with toes (don't let them cave in)\n"
            "- Descend until hip crease is at or below knee level (depth)\n"
            "- Drive through the whole foot, not just the toes, to stand up\n"
            "If depth is limited, it's usually ankle or hip mobility - try heel-"
            "elevated squats or goblet squats to a box while you build mobility."
        ),
    },
    {
        "topic": "Deadlift form",
        "q": "how to deadlift, deadlift form, rounded back deadlift, deadlift setup",
        "a": (
            "Deadlift form checklist:\n"
            "- Bar over mid-foot, shins close to the bar\n"
            "- Grip just outside your legs, flat back, chest up\n"
            "- Take the slack out of the bar before pulling (you should hear/feel it click)\n"
            "- Push the floor away with your legs first, then extend hips\n"
            "- Keep the bar close to your body the entire way up\n"
            "A rounded lower back is almost always a bracing issue - practice "
            "Romanian deadlifts lighter to groove the hip hinge pattern."
        ),
    },
    {
        "topic": "Bench press form",
        "q": "how to bench press, bench form, shoulder pain bench press",
        "a": (
            "Bench press form checklist:\n"
            "- Shoulder blades pulled back and down, slight arch, feet flat on floor\n"
            "- Grip slightly wider than shoulder width\n"
            "- Lower the bar to mid-chest, elbows at roughly 45-75 degrees from torso\n"
            "- Press up and slightly back toward your face\n"
            "If you get shoulder pain, check your elbow flare (too wide/flared "
            "increases strain) and make sure your shoulder blades stay retracted "
            "throughout, not shrugging up."
        ),
    },
    {
        "topic": "Progressive overload",
        "q": "how to get stronger, progressive overload, plateau, not gaining strength",
        "a": (
            "Progressive overload options, in order of priority:\n"
            "1. Add reps at the same weight until you hit the top of your rep range\n"
            "2. Add small weight increments (1-2.5kg upper body, 2.5-5kg lower body)\n"
            "3. Add a set\n"
            "4. Improve technique/range of motion at the same load\n"
            "If you've plateaued for 3+ weeks, check sleep and nutrition first - "
            "programming is rarely the actual bottleneck."
        ),
    },
    {
        "topic": "Warm-up",
        "q": "how to warm up, warm up before workout, injury prevention warmup",
        "a": (
            "General warm-up (5-8 minutes):\n"
            "- 3-5 min light cardio (bike, row, or jog) to raise heart rate\n"
            "- Dynamic stretches: leg swings, arm circles, hip openers\n"
            "- 2 light warm-up sets of your first exercise, working up in weight\n"
            "Skip long static stretching before lifting - save that for after, "
            "or a separate mobility session."
        ),
    },
    {
        "topic": "Rest days and recovery",
        "q": "how many rest days, recovery time, sore muscles, overtraining",
        "a": (
            "General recovery guidelines:\n"
            "- Beginners: 1 rest day between full-body sessions is usually enough\n"
            "- Intermediate/advanced: at least 1 full rest day per week, more if "
            "sleep or stress is high\n"
            "- Muscle soreness (DOMS) peaks 24-48h after training and isn't a "
            "requirement for progress - you can train a sore muscle lightly\n"
            "Signs of overtraining: persistent fatigue, declining performance, "
            "irritability, poor sleep - back off volume or intensity for a week if so."
        ),
    },
    {
        "topic": "Protein and nutrition basics",
        "q": "how much protein, nutrition for muscle gain, diet for fitness, calories",
        "a": (
            "Nutrition basics for training:\n"
            "- Protein: roughly 1.6-2.2g per kg bodyweight per day, spread across meals\n"
            "- Calories: surplus (~300-500 above maintenance) to build muscle, "
            "deficit (~300-500 below) to lose fat, maintenance to recomp slowly\n"
            "- Carbs fuel training performance, fats support hormones - don't cut "
            "either to extremes\n"
            "This is general guidance, not a personalized diet plan - a "
            "dietitian can tailor numbers to your body and goals."
        ),
    },
    {
        "topic": "Weight loss / fat loss",
        "q": "how to lose weight, fat loss tips, cutting, losing belly fat",
        "a": (
            "Fat loss fundamentals:\n"
            "- A consistent calorie deficit is the actual driver - track food for "
            "1-2 weeks if progress stalls to see where calories are hiding\n"
            "- Keep lifting during a cut to preserve muscle, don't just do cardio\n"
            "- Aim for a slow, sustainable rate: about 0.5-1% of bodyweight per week\n"
            "- Spot reduction (losing fat from one area) isn't possible - fat "
            "loss happens across the whole body"
        ),
    },
    {
        "topic": "Muscle gain / bulking",
        "q": "how to build muscle, bulking, gaining mass, skinny fat",
        "a": (
            "Muscle gain fundamentals:\n"
            "- Small calorie surplus (~300-500 over maintenance) plus progressive "
            "overload is the core driver\n"
            "- Hit protein target (1.6-2.2g/kg) consistently\n"
            "- Train each muscle group 2x per week for better growth than once\n"
            "- Prioritize sleep (7-9h) - it's when most recovery/growth happens"
        ),
    },
    {
        "topic": "Knee pain",
        "q": "knee pain squatting, knee pain running, knee hurts during exercise",
        "a": (
            "General knee pain guidance (not a diagnosis):\n"
            "- Sharp, sudden, or swelling pain: stop the movement and see a "
            "doctor or physio before continuing\n"
            "- Dull ache during/after squats or running is often volume or form "
            "related - reduce load/depth temporarily and check knee tracking\n"
            "- Strengthening quads and glutes often helps kneecap-related pain "
            "over time\n"
            "This isn't medical advice - persistent or worsening pain needs a "
            "professional assessment."
        ),
    },
    {
        "topic": "Lower back pain",
        "q": "lower back pain deadlift, back hurts after workout, back pain lifting",
        "a": (
            "General lower back guidance (not a diagnosis):\n"
            "- Sharp pain, numbness, or pain radiating down a leg: stop and see "
            "a doctor or physio\n"
            "- General tightness after deadlifts/squats is often a bracing or "
            "rounding issue - lighten the load and drill hip hinge technique\n"
            "- Core and glute strengthening (planks, bird-dogs, hip thrusts) "
            "often help general low back resilience\n"
            "This isn't medical advice - get persistent pain checked out properly."
        ),
    },
    {
        "topic": "Cardio for fitness",
        "q": "how much cardio, running for fitness, cardio and lifting together",
        "a": (
            "Cardio guidelines:\n"
            "- General health: 150 min moderate or 75 min vigorous cardio per week\n"
            "- Combining with lifting: put cardio after weights or on separate "
            "days/times so it doesn't blunt strength gains\n"
            "- For fat loss, cardio helps the calorie deficit but diet still "
            "matters more - don't rely on cardio alone to out-work poor eating"
        ),
    },
    {
        "topic": "Motivation and consistency",
        "q": "how to stay motivated, consistency tips, skipping workouts, lost motivation",
        "a": (
            "Consistency tips:\n"
            "- Schedule workouts like appointments, same days/times each week\n"
            "- Track your lifts - visible progress is the best motivation\n"
            "- Have a fallback \"minimum\" session (15 min) for busy days instead "
            "of skipping entirely\n"
            "- Missing one session doesn't matter - missing weeks in a row does. "
            "Just get back to the next scheduled session."
        ),
    },
]
