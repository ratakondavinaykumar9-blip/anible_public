#!/usr/bin/env python3
"""
Resume to PDF Generator - All Tailored Versions
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os

OUTPUT_DIR = "/home/user/.openclaw/workspace/job_applications/resumes"

def create_pdf(data, filename):
    doc = SimpleDocTemplate(filename, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=18, alignment=TA_CENTER, spaceAfter=3)
    section_style = ParagraphStyle('Section', parent=styles['Heading2'], fontSize=12, textColor=colors.HexColor("#2c3e50"), borderPadding=5, spaceAfter=6, borderWidthBottom=2, borderColor=colors.HexColor("#3498db"))
    
    for item in data:
        if item[0] == "HEADER":
            for key, value in item[1]:
                if key == "name":
                    story.append(Paragraph(value, title_style))
                elif key == "title":
                    story.append(Paragraph(f"<b>{value}</b>", ParagraphStyle('SubTitle', parent=styles['Normal'], alignment=TA_CENTER, fontSize=12, textColor=colors.HexColor("#3498db"))))
                elif key == "contact":
                    story.append(Paragraph(value, ParagraphStyle('Contact', parent=styles['Normal'], alignment=TA_CENTER, fontSize=9, textColor=colors.gray)))
            story.append(Spacer(1, 20))
        elif item[0] == "SECTION":
            story.append(Paragraph(item[1], section_style))
        elif item[0] == "TEXT":
            story.append(Paragraph(item[1], styles['Normal']))
            story.append(Spacer(1, 10))
        elif item[0] == "BULLETS":
            for bullet in item[1]:
                story.append(Paragraph(f"• {bullet}", styles['Normal']))
            story.append(Spacer(1, 10))
        elif item[0] == "EXPERIENCE":
            exp = item[1]
            story.append(Paragraph(f"<b>{exp['title']}</b> | {exp['company']} | {exp['period']}", styles['Normal']))
            for highlight in exp['highlights']:
                story.append(Paragraph(f"• {highlight}", styles['Normal']))
            story.append(Spacer(1, 10))
        elif item[0] == "PROJECT":
            proj = item[1]
            story.append(Paragraph(f"<b>{proj['title']}</b>", styles['Normal']))
            for point in proj['points']:
                story.append(Paragraph(f"• {point}", styles['Normal']))
            story.append(Spacer(1, 8))
        elif item[0] == "TABLE":
            t = Table(item[1], colWidths=[1.5*inch, 4.5*inch])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f5f5f5")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#dddddd")),
            ]))
            story.append(t)
            story.append(Spacer(1, 15))
    doc.build(story)
    print(f"Created: {filename}")

# Standard Resume
standard = [
    ("HEADER", [("name", "RATAGONDA VINAYKUMAR"), ("title", "Network Security Engineer"), ("contact", "Ontario, Canada | ratakondavinaykumar9@gmail.com | linkedin.com/in/vinaykumar")]),
    ("SECTION", "PROFESSIONAL SUMMARY"),
    ("TEXT", "Results-driven Network Security Engineer with 3+ years of experience in designing, implementing, and managing enterprise security infrastructure. Proven expertise in firewall security, cloud security (Azure), and network automation using Ansible."),
    ("SECTION", "CORE COMPETENCIES"),
    ("BULLETS", [
        "Firewall Security: Cisco FTD, FMC, ASA, FortiGate, Palo Alto",
        "Cloud Security: Azure Firewall, NSG, ASG, VNET, UDR, NAT Gateway",
        "Network Security: SSL Decryption, IPS/IDS, High Availability, Clustering",
        "Identity & Access: Cisco ISE, TACACS+, RADIUS, Role-Based Access Control",
        "Automation: Ansible (200+ playbooks), Python Scripting",
        "Monitoring: SolarWinds NPM/NTA, SNMPv3, Azure Monitor",
    ]),
    ("SECTION", "PROFESSIONAL EXPERIENCE"),
    ("EXPERIENCE", {
        "title": "Network Security Engineer", "company": "SITA, Canada", "period": "2022 – Present",
        "highlights": [
            "Administered Cisco FTD, FMC, ASA, and FortiGate firewalls for enterprise clients",
            "Designed and implemented Azure Firewall policies for cloud security",
            "Configured Azure NSG rules and ASGs for micro-segmentation",
            "Built VNET peering and hub-spoke architectures with UDR",
            "Implemented Azure NAT Gateway for outbound traffic",
            "Configured SSL inspection policies for threat detection",
            "Tuned IPS/IDS rules for advanced threat protection",
            "Designed firewall clustering and failover for 99.99% uptime",
            "Developed 200+ Ansible playbooks for security automation",
            "Led zero-downtime firewall migration projects",
        ]
    }),
    ("SECTION", "CERTIFICATIONS"),
    ("BULLETS", ["CCNP Security - Cisco", "CCNA - Cisco", "Azure Security Administrator Associate - Microsoft (In Progress)"]),
    ("SECTION", "EDUCATION"),
    ("BULLETS", ["Master of Applied Science - Electronics & Computer Engineering, University of Windsor", "B.Tech - Electronics & Communication Engineering"]),
]

# Deloitte - Firewall Ops
deloitte = [
    ("HEADER", [("name", "RATAGONDA VINAYKUMAR"), ("title", "Firewall Operations Engineer"), ("contact", "Ontario, Canada | ratakondavinaykumar9@gmail.com | linkedin.com/in/vinaykumar")]),
    ("SECTION", "APPLICATION: DELOITTE - Firewall Operations Engineer"),
    ("SECTION", "WHY I'M A GREAT FIT"),
    ("BULLETS", [
        "3+ years administering enterprise firewalls (Cisco ASA, FTD, FortiGate)",
        "Expertise in SSL decryption, IPS/IDS, high availability clustering",
        "Azure Firewall, NSG, ASG, VNET, UDR - cloud security implementation",
        "Built 200+ Ansible playbooks for security automation",
    ]),
    ("SECTION", "PROFESSIONAL EXPERIENCE"),
    ("EXPERIENCE", {
        "title": "Network Security Engineer", "company": "SITA, Canada", "period": "2022 – Present",
        "highlights": [
            "Administered enterprise firewalls ensuring 99.99% uptime",
            "Deployed Azure Firewall and cloud security infrastructure",
            "Implemented SSL inspection and IPS/IDS for threat protection",
            "Built high availability firewall clusters",
            "Developed Ansible automation for security operations",
            "Led zero-downtime firewall migration projects",
        ]
    }),
    ("SECTION", "KEY SKILLS"),
    ("TABLE", [
        ["Skill", "Level"],
        ["Cisco ASA/FTD", "Expert"],
        ["FortiGate", "Expert"],
        ["Palo Alto", "Learning"],
        ["Azure Firewall/NSG", "Expert"],
        ["Ansible", "Expert"],
        ["CCNP Security", "Obtained"],
    ]),
    ("SECTION", "CERTIFICATIONS"),
    ("BULLETS", ["CCNP Security - Cisco", "CCNA - Cisco", "Azure Security Administrator Associate - In Progress"]),
    ("SECTION", "EDUCATION"),
    ("BULLETS", ["Master of Applied Science - Electronics & Computer Engineering, University of Windsor", "B.Tech - Electronics & Communication Engineering"]),
]

# Scotiabank
scotiabank = [
    ("HEADER", [("name", "RATAGONDA VINAYKUMAR"), ("title", "Network Security Engineer"), ("contact", "Ontario, Canada | ratakondavinaykumar9@gmail.com | linkedin.com/in/vinaykumar")]),
    ("SECTION", "APPLICATION: SCOTIABANK - Network Security Engineer"),
    ("SECTION", "BANKING SECTOR RELEVANT EXPERIENCE"),
    ("BULLETS", [
        "3+ years in enterprise network security",
        "Experience with compliance and security standards",
        "SSL/TLS decryption for financial data protection",
        "High availability clustering for critical systems",
        "Azure cloud security implementation",
    ]),
    ("SECTION", "PROFESSIONAL EXPERIENCE"),
    ("EXPERIENCE", {
        "title": "Network Security Engineer", "company": "SITA, Canada", "period": "2022 – Present",
        "highlights": [
            "Administered enterprise firewalls for mission-critical infrastructure",
            "Deployed Azure Firewall and cloud security for enterprise workloads",
            "Implemented SSL inspection policies for financial data protection",
            "Configured IPS/IDS rules for advanced threat detection",
            "Built high availability firewall clusters (99.99% uptime)",
            "Developed Ansible automation (200+ playbooks)",
        ]
    }),
    ("SECTION", "KEY SKILLS"),
    ("TABLE", [
        ["Skill", "Experience"],
        ["Firewall Management", "3+ years (ASA, FTD, FortiGate)"],
        ["Cloud Security", "Azure Firewall, NSG, ASG, VNET"],
        ["SSL Decryption", "Implemented for threat detection"],
        ["Automation", "Ansible, Python"],
    ]),
    ("SECTION", "CERTIFICATIONS"),
    ("BULLETS", ["CCNP Security - Cisco", "CCNA - Cisco", "Azure Security Administrator Associate - In Progress"]),
    ("SECTION", "EDUCATION"),
    ("BULLETS", ["Master of Applied Science - University of Windsor", "B.Tech - Electronics & Communication"]),
]

# TD Bank - Azure
td_azure = [
    ("HEADER", [("name", "RATAGONDA VINAYKUMAR"), ("title", "Azure Security Engineer"), ("contact", "Ontario, Canada | ratakondavinaykumar9@gmail.com | linkedin.com/in/vinaykumar")]),
    ("SECTION", "APPLICATION: TD BANK - Security Engineer (Azure Focus)"),
    ("SECTION", "AZURE EXPERTISE"),
    ("BULLETS", [
        "Azure Firewall - designed and implemented policies",
        "NSG & ASG - configured for micro-segmentation",
        "UDR - custom routing implementation",
        "VNET - hub-spoke and peering architectures",
        "NAT Gateway - outbound traffic management",
        "Azure AD - identity-based security integration",
    ]),
    ("SECTION", "PROFESSIONAL EXPERIENCE"),
    ("EXPERIENCE", {
        "title": "Network Security Engineer", "company": "SITA, Canada", "period": "2022 – Present",
        "highlights": [
            "Designed and implemented Azure Firewall policies for enterprise cloud workloads",
            "Configured NSG and ASG rules for micro-segmentation",
            "Built VNET peering and hub-spoke architectures with UDR",
            "Implemented Azure NAT Gateway for outbound traffic",
            "Integrated with Azure AD for identity-based access",
            "Administered Cisco ASA, FTD, FortiGate firewalls",
        ]
    }),
    ("SECTION", "AZURE SKILLS MATRIX"),
    ("TABLE", [
        ["Service", "Experience"],
        ["Azure Firewall", "Designed & implemented policies"],
        ["NSG", "Rule configuration, micro-segmentation"],
        ["ASG", "Application-based grouping"],
        ["VNET", "Hub-spoke, peering"],
        ["UDR", "Custom routing"],
        ["NAT Gateway", "Outbound management"],
        ["Azure AD", "Identity integration"],
    ]),
    ("SECTION", "CERTIFICATIONS"),
    ("BULLETS", ["CCNP Security - Cisco", "CCNA - Cisco", "Azure Security Administrator Associate - In Progress"]),
    ("SECTION", "EDUCATION"),
    ("BULLETS", ["Master of Applied Science - University of Windsor", "B.Tech - Electronics & Communication"]),
]

# Bell Canada
bell = [
    ("HEADER", [("name", "RATAGONDA VINAYKUMAR"), ("title", "Network Security Engineer"), ("contact", "Ontario, Canada | ratakondavinaykumar9@gmail.com | linkedin.com/in/vinaykumar")]),
    ("SECTION", "APPLICATION: BELL CANADA - Senior Network Security Engineer"),
    ("SECTION", "TELECOM-RELEVANT EXPERIENCE"),
    ("BULLETS", [
        "3+ years at SITA - global IT provider for aviation industry",
        "Experience with large-scale network infrastructure",
        "High availability and performance for 24/7 operations",
        "Enterprise firewall management (Cisco ASA, FTD, FortiGate)",
        "Azure cloud security implementation",
    ]),
    ("SECTION", "PROFESSIONAL EXPERIENCE"),
    ("EXPERIENCE", {
        "title": "Network Security Engineer", "company": "SITA, Canada", "period": "2022 – Present",
        "highlights": [
            "Administered enterprise firewalls for global aviation network",
            "Deployed Azure cloud security infrastructure",
            "Implemented SSL inspection and IPS/IDS",
            "Built high availability firewall clusters",
            "Developed Ansible automation (200+ playbooks)",
            "Led zero-downtime migration projects",
        ]
    }),
    ("SECTION", "SKILLS FOR BELL"),
    ("TABLE", [
        ["Skill", "Level"],
        ["Cisco ASA/FTD", "Expert"],
        ["FortiGate", "Expert"],
        ["Azure Security", "Expert"],
        ["Ansible", "Expert"],
        ["CCNP Security", "Obtained"],
    ]),
    ("SECTION", "CERTIFICATIONS"),
    ("BULLETS", ["CCNP Security - Cisco", "CCNA - Cisco", "Azure Security Administrator - In Progress"]),
    ("SECTION", "EDUCATION"),
    ("BULLETS", ["Master of Applied Science - University of Windsor", "B.Tech - Electronics & Communication"]),
]

# SOC Engineer
soc = [
    ("HEADER", [("name", "RATAGONDA VINAYKUMAR"), ("title", "SOC Engineer"), ("contact", "Ontario, Canada | ratakondavinaykumar9@gmail.com | linkedin.com/in/vinaykumar")]),
    ("SECTION", "APPLICATION: SOC Engineer / Analyst"),
    ("SECTION", "SOC-RELEVANT SKILLS"),
    ("BULLETS", [
        "IPS/IDS configuration and tuning",
        "SSL/TLS decryption for traffic analysis",
        "Firewall rule analysis and optimization",
        "Real-time monitoring with SolarWinds, Azure Monitor",
        "Log analysis and correlation",
    ]),
    ("SECTION", "EXPERIENCE"),
    ("EXPERIENCE", {
        "title": "Network Security Engineer", "company": "SITA", "period": "2022 – Present",
        "highlights": [
            "Monitored network for security threats",
            "Responded to security incidents",
            "Tuned IPS/IDS rules",
            "Analyzed firewall logs",
            "Built automation for SOC workflows",
        ]
    }),
    ("SECTION", "SKILLS"),
    ("TABLE", [
        ["Category", "Skills"],
        ["Monitoring", "SolarWinds, Azure Monitor, SNMP"],
        ["Threat Detection", "IPS/IDS, SSL Decryption"],
        ["Firewalls", "Cisco ASA, FTD, FortiGate"],
        ["Automation", "Ansible, Python"],
    ]),
    ("SECTION", "CERTIFICATIONS"),
    ("BULLETS", ["CCNP Security, CCNA", "Azure Security Administrator - In Progress"]),
]

# Cybersecurity
cybersec = [
    ("HEADER", [("name", "RATAGONDA VINAYKUMAR"), ("title", "Cybersecurity Engineer"), ("contact", "Ontario, Canada | ratakondavinaykumar9@gmail.com | linkedin.com/in/vinaykumar")]),
    ("SECTION", "APPLICATION: Cybersecurity Engineer Positions"),
    ("SECTION", "CYBERSECURITY EXPERTISE"),
    ("BULLETS", [
        "SSL/TLS Decryption - implemented for threat detection",
        "IPS/IDS - configured and tuned rules for advanced threat protection",
        "Firewall policy management - Cisco ASA, FTD, FortiGate",
        "Azure Firewall, NSG, ASG - cloud security",
        "200+ Ansible playbooks for security automation",
    ]),
    ("SECTION", "PROFESSIONAL EXPERIENCE"),
    ("EXPERIENCE", {
        "title": "Network Security Engineer", "company": "SITA, Canada", "period": "2022 – Present",
        "highlights": [
            "Implemented cybersecurity measures for enterprise network",
            "Deployed Azure Firewall and cloud security",
            "Configured SSL decryption and IPS/IDS",
            "Built firewall clustering for 99.99% uptime",
            "Developed Ansible automation for security operations",
        ]
    }),
    ("SECTION", "SECURITY SKILLS"),
    ("TABLE", [
        ["Category", "Skills"],
        ["Firewalls", "Cisco ASA/FTD, FortiGate, Palo Alto"],
        ["Cloud Security", "Azure Firewall, NSG, ASG, VNET"],
        ["Threat Protection", "SSL Decryption, IPS/IDS"],
        ["Identity", "Cisco ISE, TACACS+, Azure AD"],
        ["Automation", "Ansible, Python"],
    ]),
    ("SECTION", "CERTIFICATIONS"),
    ("BULLETS", ["CCNP Security - Cisco", "CCNA - Cisco", "Azure Security Administrator Associate - In Progress"]),
    ("SECTION", "EDUCATION"),
    ("BULLETS", ["Master of Applied Science - University of Windsor", "B.Tech - Electronics & Communication"]),
]

# Generate all PDFs
os.makedirs(OUTPUT_DIR, exist_ok=True)

create_pdf(standard, f"{OUTPUT_DIR}/Vinay_Resume_Standard.pdf")
create_pdf(deloitte, f"{OUTPUT_DIR}/Vinay_Resume_Deloitte.pdf")
create_pdf(scotiabank, f"{OUTPUT_DIR}/Vinay_Resume_Scotiabank.pdf")
create_pdf(td_azure, f"{OUTPUT_DIR}/Vinay_Resume_TD_Bank_Azure.pdf")
create_pdf(bell, f"{OUTPUT_DIR}/Vinay_Resume_Bell_Canada.pdf")
create_pdf(soc, f"{OUTPUT_DIR}/Vinay_Resume_SOC_Engineer.pdf")
create_pdf(cybersec, f"{OUTPUT_DIR}/Vinay_Resume_Cybersecurity.pdf")

print("\n✅ All 7 PDF resumes generated!")
print(f"Location: {OUTPUT_DIR}/")
