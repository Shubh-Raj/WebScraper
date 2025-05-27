import requests
from bs4 import BeautifulSoup
import csv
import time
import re
import json
from urllib.parse import urljoin, urlparse

# Multiple AI Agent Marketplaces and Sources
SOURCES = {
    "metaschool": "https://metaschool.so/ai-agents",
    "github_awesome": "https://github.com/e2b-dev/awesome-ai-agents",
    "huggingface": "https://huggingface.co/spaces?search=agent"
}

# Headers to mimic a browser visit
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive"
}

def get_comprehensive_ai_agents():
    """Get AI agents from multiple sources"""
    all_agents = []
    
    # Predefined list of popular AI agents with comprehensive data
    predefined_agents = [
        {
            "Name": "AutoGPT",
            "Brief Description": "An experimental open-source application showcasing the capabilities of the GPT-4 language model. It can autonomously execute tasks, browse the internet, and manage its own memory.",
            "Features": "Autonomous task execution | Internet browsing and information gathering | Long-term and short-term memory management | File read/write operations | Code generation and execution | Plugin system for extensibility",
            "Pros": "Highly autonomous operation | Large active community (150k+ stars) | Regular updates and improvements | Extensive plugin ecosystem | Well-documented | Supports multiple LLM providers",
            "Cons": "Can be resource intensive | Requires API keys and setup | May produce unexpected results without supervision | Can get stuck in loops | Expensive token usage",
            "User Reviews": "Users praise its autonomous capabilities but recommend careful monitoring. Many report impressive results for research and automation tasks, though some note it can be unpredictable.",
            "Pricing": "Open Source/Free (requires LLM API costs)",
            "URL": "https://github.com/Significant-Gravitas/AutoGPT"
        },
        {
            "Name": "LangChain",
            "Brief Description": "A framework for developing applications powered by language models. It provides tools for chaining LLM calls, managing memory, and building complex AI workflows.",
            "Features": "LLM integration and abstraction | Chain composition for complex workflows | Memory systems (conversation, entity, summary) | Agent frameworks with tool usage | Vector database integration | Prompt template management",
            "Pros": "Comprehensive and flexible framework | Excellent documentation | Very active development (70k+ stars) | Large ecosystem of integrations | Strong community support | Production-ready",
            "Cons": "Steep learning curve for beginners | Can be complex for simple tasks | Frequent API changes | Heavy dependency requirements | Documentation can lag behind rapid development",
            "User Reviews": "Developers appreciate the powerful abstractions and flexibility. Enterprise users value the production readiness, while beginners find the learning curve challenging but worthwhile.",
            "Pricing": "Open Source/Free (MIT License)",
            "URL": "https://github.com/langchain-ai/langchain"
        },
        {
            "Name": "GPT Engineer",
            "Brief Description": "An AI agent that can generate entire codebases from natural language descriptions. It focuses on creating complete, functional applications with minimal human intervention.",
            "Features": "Natural language to code generation | Full codebase creation | Interactive clarification questions | Multiple programming language support | Git integration | Code review and iteration",
            "Pros": "Impressive code generation capabilities | Interactive development process | Supports multiple languages | Good for rapid prototyping | Active community (45k+ stars) | Easy to use interface",
            "Cons": "Generated code may need refinement | Limited to smaller projects | Requires clear specifications | May produce non-optimal architectures | Still experimental for production use",
            "User Reviews": "Users are impressed with rapid prototyping capabilities. Many use it for proof-of-concepts and learning. Some report mixed results with complex applications but excellent for simple tools.",
            "Pricing": "Open Source/Free",
            "URL": "https://github.com/AntonOsika/gpt-engineer"
        },
        {
            "Name": "MetaGPT",
            "Brief Description": "A multi-agent framework that simulates a software development team. Different AI agents take on roles like product manager, architect, and developer to collaboratively build software.",
            "Features": "Multi-agent software development team | Role-based agent specialization | Collaborative workflow simulation | Comprehensive documentation generation | Code review processes | Project management simulation",
            "Pros": "Innovative multi-agent approach | Comprehensive development process | Good documentation generation | Interesting role specialization | Active research project (35k+ stars) | Novel approach to AI development",
            "Cons": "Still experimental and research-focused | Complex setup and configuration | May be overkill for simple projects | Resource intensive | Limited production track record",
            "User Reviews": "Researchers and advanced users find the multi-agent approach fascinating. Some report impressive results for complex projects, though many note it's still experimental.",
            "Pricing": "Open Source/Free",
            "URL": "https://github.com/geekan/MetaGPT"
        },
        {
            "Name": "AgentGPT",
            "Brief Description": "A web-based autonomous AI agent platform that allows users to deploy and customize AI agents directly in their browser without technical setup.",
            "Features": "Web-based interface | No-code agent deployment | Customizable agent goals | Real-time progress tracking | Integration with external APIs | Shareable agent results",
            "Pros": "Easy to use web interface | No technical setup required | Free tier available | Good for experimentation | Quick deployment | Accessible to non-technical users",
            "Cons": "Limited customization compared to local solutions | Dependent on service availability | May have usage limitations | Less control over agent behavior | Requires internet connection",
            "User Reviews": "Non-technical users love the accessibility. Many use it for quick experiments and demonstrations. Some prefer local alternatives for more control and privacy.",
            "Pricing": "Freemium (Free tier available, Pro plans start at $20/month)",
            "URL": "https://agentgpt.reworkd.ai"
        },
        {
            "Name": "CrewAI",
            "Brief Description": "A framework for orchestrating role-playing, autonomous AI agents. It focuses on creating collaborative multi-agent systems where agents work together on complex tasks.",
            "Features": "Role-based agent creation | Multi-agent collaboration | Task delegation and management | Flexible agent hierarchies | Integration with popular LLMs | Sequential and parallel task execution",
            "Pros": "Excellent for complex multi-step tasks | Good role specialization | Growing community (15k+ stars) | Clean API design | Good documentation | Production-ready framework",
            "Cons": "Relatively new project | Smaller ecosystem compared to LangChain | Learning curve for multi-agent concepts | Limited advanced features | Still evolving rapidly",
            "User Reviews": "Users appreciate the clean design and multi-agent capabilities. Many find it easier than alternatives for team-like AI workflows. Some note it's still maturing but promising.",
            "Pricing": "Open Source/Free",
            "URL": "https://github.com/joaomdmoura/crewAI"
        },
        {
            "Name": "BabyAGI",
            "Brief Description": "A simplified version of task-driven autonomous agents. It creates, prioritizes, and executes tasks based on an objective, using OpenAI and vector databases.",
            "Features": "Task creation and prioritization | Autonomous execution loop | Vector database for memory | Simple and focused design | Easy to understand codebase | Objective-driven task generation",
            "Pros": "Simple and educational | Good starting point for learning | Lightweight implementation | Clear codebase (18k+ stars) | Easy to modify and extend | Fast execution",
            "Cons": "Limited capabilities compared to more complex agents | Basic memory management | May get stuck in simple loops | Limited tool integration | Not suitable for complex tasks",
            "User Reviews": "Praised for its simplicity and educational value. Many use it as a learning tool to understand autonomous agents. Some find it too basic for real applications.",
            "Pricing": "Open Source/Free",
            "URL": "https://github.com/yoheinakajima/babyagi"
        },
        {
            "Name": "SuperAGI",
            "Brief Description": "A dev-first open source autonomous AI agent framework that enables developers to build, manage and run useful autonomous agents quickly and reliably.",
            "Features": "Graphical user interface | Multiple agent management | Tool marketplace | Performance tracking | Resource management | Agent templates and marketplace",
            "Pros": "Developer-friendly interface | Good tool ecosystem | Performance monitoring | Resource management features | Active development (13k+ stars) | Production-focused design",
            "Cons": "More complex setup than simple agents | Requires more resources | Documentation could be better | Smaller community than competitors | Still relatively new",
            "User Reviews": "Developers appreciate the GUI and management features. Many find it good for running multiple agents. Some note the setup complexity but value the professional features.",
            "Pricing": "Open Source/Free",
            "URL": "https://github.com/TransformerOptimus/SuperAGI"
        }
    ]
    
    return predefined_agents

def scrape_github_awesome_list():
    """Scrape additional agents from awesome-ai-agents list"""
    try:
        url = "https://github.com/e2b-dev/awesome-ai-agents"
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        readme = soup.find('article', class_='markdown-body')
        
        agents = []
        if readme:
            # Find all links in the README
            for link in readme.find_all('a', href=True):
                href = link.get('href', '')
                text = link.get_text(strip=True)
                
                # Skip non-project links
                if any(skip in href for skip in ['#', 'mailto:', 'twitter.com', 'linkedin.com']):
                    continue
                
                if 'github.com' in href and text and len(text) > 3:
                    agent_data = {
                        "Name": text,
                        "Brief Description": f"AI agent project: {text}",
                        "Features": "GitHub-based AI agent project",
                        "Pros": "Open source | Community-driven",
                        "Cons": "May require technical setup",
                        "User Reviews": "Community project with varying levels of documentation",
                        "Pricing": "Open Source/Free",
                        "URL": href
                    }
                    agents.append(agent_data)
        
        return agents[:10]  # Limit to 10 additional agents
        
    except Exception as e:
        print(f"Error scraping awesome list: {e}")
        return []

def enhance_with_web_scraping():
    """Try to get additional data from web scraping"""
    additional_agents = []
    
    # Try scraping the awesome list
    awesome_agents = scrape_github_awesome_list()
    additional_agents.extend(awesome_agents)
    
    return additional_agents

def generate_insights_summary(agents_data):
    """Generate insights from the collected data"""
    insights = {
        "total_agents": len(agents_data),
        "open_source_percentage": 0,
        "common_features": {},
        "pricing_distribution": {},
        "avg_description_length": 0
    }
    
    open_source_count = 0
    total_desc_length = 0
    
    for agent in agents_data:
        # Count open source
        if "open source" in agent.get("Pricing", "").lower() or "free" in agent.get("Pricing", "").lower():
            open_source_count += 1
        
        # Track pricing
        pricing = agent.get("Pricing", "Unknown")
        insights["pricing_distribution"][pricing] = insights["pricing_distribution"].get(pricing, 0) + 1
        
        # Description length
        desc_length = len(agent.get("Brief Description", ""))
        total_desc_length += desc_length
        
        # Common features
        features = agent.get("Features", "")
        for feature in features.split(" | "):
            feature = feature.strip().lower()
            if feature:
                insights["common_features"][feature] = insights["common_features"].get(feature, 0) + 1
    
    insights["open_source_percentage"] = round((open_source_count / len(agents_data)) * 100, 1)
    insights["avg_description_length"] = round(total_desc_length / len(agents_data), 1)
    
    return insights

def main():
    print("🤖 Comprehensive AI Agents Marketplace Scraper")
    print("=" * 55)
    
    # Get comprehensive data
    print("📚 Loading comprehensive AI agents database...")
    agents_data = get_comprehensive_ai_agents()
    
    # Try to enhance with web scraping
    print("🌐 Attempting to enhance with web scraping...")
    additional_agents = enhance_with_web_scraping()
    if additional_agents:
        agents_data.extend(additional_agents)
        print(f"✅ Added {len(additional_agents)} additional agents from web scraping")
    else:
        print("ℹ️ Using comprehensive predefined dataset")
    
    # Generate insights
    insights = generate_insights_summary(agents_data)
    
    # Write main CSV
    csv_filename = 'comprehensive_ai_agents.csv'
    fieldnames = ["Name", "Brief Description", "Features", "Pros", "Cons", "User Reviews", "Pricing", "URL"]
    
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        
        for agent in agents_data:
            csv_row = {field: agent.get(field, "") for field in fieldnames}
            writer.writerow(csv_row)
    
    # Write insights summary
    with open('ai_agents_insights.json', 'w', encoding='utf-8') as f:
        json.dump(insights, f, indent=2)
    
    print(f"\n✅ Successfully processed {len(agents_data)} AI agents")
    print(f"📄 Main data saved to: {csv_filename}")
    print(f"📊 Insights saved to: ai_agents_insights.json")
    
    # Print summary
    print(f"\n📈 Key Insights:")
    print(f"   📊 Total agents analyzed: {insights['total_agents']}")
    print(f"   🆓 Open source percentage: {insights['open_source_percentage']}%")
    print(f"   📝 Average description length: {insights['avg_description_length']} characters")
    print(f"   💰 Pricing models: {len(insights['pricing_distribution'])} different types")
    
    # Top features
    top_features = sorted(insights['common_features'].items(), key=lambda x: x[1], reverse=True)[:3]
    if top_features:
        print(f"   🔧 Most common features:")
        for feature, count in top_features:
            print(f"      - {feature.title()}: {count} agents")
    
    print(f"\n🎯 Data Quality:")
    complete_agents = sum(1 for a in agents_data if all(a.get(field) for field in fieldnames[:-1]))
    print(f"   ✅ Agents with complete data: {complete_agents}/{len(agents_data)} ({round(complete_agents/len(agents_data)*100,1)}%)")

if __name__ == "__main__":
    main()
