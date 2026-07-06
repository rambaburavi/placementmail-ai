import re


class KeywordAnalyzer:

    def analyze(self, email):

        text = (
            email.get("subject", "") + " " +
            email.get("plain_text", "")
        ).lower()

        category = "Other"
        priority = "Medium"
        placement = False
        company = ""

        company_patterns = [
            r"google",
            r"microsoft",
            r"amazon",
            r"qualcomm",
            r"zoho",
            r"tcs",
            r"infosys",
            r"wipro",
            r"accenture",
            r"cognizant",
        ]

        for pattern in company_patterns:
            if re.search(pattern, text):
                company = pattern.title()
                break

        if "interview" in text:
            category = "Interview"
            priority = "High"
            placement = True

        elif "assessment" in text:
            category = "Coding Assessment"
            priority = "High"
            placement = True

        elif "offer" in text:
            category = "Offer Letter"
            priority = "Critical"
            placement = True

        elif "intern" in text:
            category = "Internship"
            priority = "Medium"
            placement = True

        elif "hackathon" in text:
            category = "Hackathon"
            priority = "Medium"
            placement = True

        elif "reject" in text:
            category = "Rejection"
            priority = "Low"
            placement = True

        return {
            "category": category,
            "priority": priority,
            "placement_related": placement,
            "company": company,
            "deadline": "",
            "summary": "Generated using keyword fallback",
            "action_required": "Review manually",
            "confidence": 0.30,
            "ai_provider": "Keyword",
            "analysis_status": "FALLBACK",
        }