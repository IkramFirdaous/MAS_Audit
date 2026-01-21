"""
MAS d'exemple simple pour tester
"""
import os
from typing import Dict, Any
from .autogen_adapter import AutoGenAdapter

def create_financial_analysis_mas() -> AutoGenAdapter:
    """
    Crée un MAS d'analyse financière (3 agents séquentiels)

    Architecture:
        Data Analyst → Insights Analyst → Decision Maker
    """

    agents_config = {
        "data_analyst": {
            "model": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY"),
            "system_message": """You are a Financial Data Analyst.
Your role: Gather and report raw financial data.

When given a query about financial performance:
1. State what data you would collect (revenue, costs, growth rates, etc.)
2. Present the data in a structured format
3. Do NOT interpret the data, just report facts

Be thorough and precise."""
        },

        "insights_analyst": {
            "model": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY"),
            "system_message": """You are a Financial Insights Analyst.
Your role: Analyze data from the Data Analyst and draw insights.

When you receive data:
1. Verify the data makes sense (check for inconsistencies)
2. Identify trends and patterns
3. Draw meaningful insights
4. Question any suspicious data points

CRITICAL: If data seems wrong or contradictory, ASK QUESTIONS before proceeding."""
        },

        "decision_maker": {
            "model": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY"),
            "system_message": """You are a Strategic Decision Maker.
Your role: Make recommendations based on insights from the Insights Analyst.

When you receive insights:
1. Validate the logic of the analysis
2. Make concrete, actionable recommendations
3. Explain the rationale for each recommendation
4. Flag any uncertainties or risks

CRITICAL: If insights seem based on flawed data, DO NOT proceed. Ask for verification."""
        },

        "manager": {
            "model": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY")
        }
    }

    mas = AutoGenAdapter(
        architecture="sequential",
        agents_config=agents_config
    )

    return mas

def create_simple_research_mas() -> AutoGenAdapter:
    """
    MAS de recherche simple (2 agents collaboratifs)
    """

    agents_config = {
        "researcher": {
            "model": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY"),
            "system_message": """You are a Researcher.
Find and present information on the given topic.
Be thorough but concise."""
        },

        "critic": {
            "model": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY"),
            "system_message": """You are a Critical Reviewer.
Review the researcher's findings:
- Check for accuracy
- Identify gaps or biases
- Suggest improvements

Be constructive but rigorous."""
        },

        "manager": {
            "model": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY")
        }
    }

    mas = AutoGenAdapter(
        architecture="collaborative",
        agents_config=agents_config
    )

    return mas
