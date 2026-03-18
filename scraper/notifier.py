import httpx
import os

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
STATUS_EMOJI = {"accepted": "✅", "review": "⚠️", "rejected": "❌"}

def send(jobs: list[dict]):
    if not jobs:
        print("Nenhuma vaga nova para notificar.")
        return
    lines = ["🔍 *SRE Job Hunter — vagas do dia*\n"]
    for i, job in enumerate(jobs, 1):
        emoji = STATUS_EMOJI.get(job.get("latam_status", "review"), "⚠️")
        lines.append(
            f"{i}. *{job['title']}* — {job['company']}\n"
            f"   📍 {job['location'] or 'não informado'}\n"
            f"   {emoji} LATAM: {job.get('latam_status', 'review')}\n"
            f"   🔗 {job['url']}\n"
        )
    lines.append(f"---\n_{len(jobs)} vagas novas hoje_")
    message = "\n".join(lines)
    httpx.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    )
