/*
# Create Raven chat message history

1. New Tables
- `chat_messages`
- `id` (uuid, primary key) uniquely identifies each message.
- `session_id` (text, not null) groups messages from one browser conversation.
- `role` (text, not null) stores whether the message came from the visitor or Raven.
- `content` (text, not null) stores the message text.
- `created_at` (timestamptz) records when the message was created.

2. Security
- Enable row level security on `chat_messages`.
- Allow anonymous and authenticated visitors to read and create shared chat history.
- Allow anonymous and authenticated visitors to update or delete messages so the no-sign-in experience remains fully manageable.

3. Important Notes
- This is a single-tenant, no-sign-in chatbot, so messages are intentionally shared through the public chat surface.
- The application still limits writes to the supported message roles at the API boundary.
*/

CREATE TABLE IF NOT EXISTS public.chat_messages (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id text NOT NULL,
  role text NOT NULL CHECK (role IN ('user', 'assistant')),
  content text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS chat_messages_session_created_idx
  ON public.chat_messages (session_id, created_at);

ALTER TABLE public.chat_messages ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Public can read chat messages" ON public.chat_messages;
CREATE POLICY "Public can read chat messages"
  ON public.chat_messages FOR SELECT
  TO anon, authenticated
  USING (true);

DROP POLICY IF EXISTS "Public can create chat messages" ON public.chat_messages;
CREATE POLICY "Public can create chat messages"
  ON public.chat_messages FOR INSERT
  TO anon, authenticated
  WITH CHECK (role IN ('user', 'assistant'));

DROP POLICY IF EXISTS "Public can update chat messages" ON public.chat_messages;
CREATE POLICY "Public can update chat messages"
  ON public.chat_messages FOR UPDATE
  TO anon, authenticated
  USING (true)
  WITH CHECK (role IN ('user', 'assistant'));

DROP POLICY IF EXISTS "Public can delete chat messages" ON public.chat_messages;
CREATE POLICY "Public can delete chat messages"
  ON public.chat_messages FOR DELETE
  TO anon, authenticated
  USING (true);