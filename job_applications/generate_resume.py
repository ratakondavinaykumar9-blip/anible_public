#!/usr/bin/env python3
"""
Resume to PDF Generator
Usage: python3 generate_resume.py
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os

# Output directory
OUTPUT_DIR = "/home/user/.openclaw/workspace/job_applications/resumes"

# Resume data - Standard Resume
standard_resume = [
    ("HEADER", [
        ("name", "RATAGONDA VINAYKUMAR"),
        ("title", "Network Security Engineer"),
        ("contact", "Ontario, Canada | ratakondavinaykumar9@gmail.com | linkedin.com/in/vinaykumar"),
    ]),
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
        "Networking: TCP/IP, VLANs, OSPF, BGP, EIGRP",
    ]),
    
    ("SECTION", "PROFESSIONAL EXPERIENCE"),
    ("EXPERIENCE", {
        "title": "Network Security Engineer",
        "company": "SITA, Canada",
        "period": "2022 – Present",
        "highlights": [
            "Administered Cisco FTD, FMC, ASA, and FortiGate firewalls for enterprise clients",
            "Designed and implemented Azure Firewall policies for cloud security",
            "Configured Azure NSG rules and ASGs for micro-segmentation",
            "Built VNET peering and hub-spoke architectures with UDR",
            "Implemented Azure NAT Gateway for outbound traffic",
            "Configured SSL inspection policies for threat detection",
            "Tuned IPS/IDS rules for advanced threat protection",
            "Designed firewall clustering and failover for 99.99% uptime",
            "Integrated Cisco ISE with TACACS+ for centralized authentication",
            "Developed 200+ Ansible playbooks for security automation",
            "Led zero-downtime firewall migration projects",
            "Monitored using SolarWinds, SNMPv3, Azure Monitor",
        ]
    }),
    
    ("SECTION", "TECHNICAL PROJECTS"),
    ("PROJECT", {
        "title": "Azure Cloud Security Architecture",
        "points": [
            "Designed Azure Firewall policies for enterprise cloud workloads",
            "Configured NSG/ASG for micro-segmentation",
            "Built VNET peering with UDR for traffic routing",
            "Implemented NAT Gateway for outbound management",
        ]
    }),
    ("PROJECT", {
        "title": "Security Automation with Ansible",
        "points": [
            "Developed 200+ Ansible playbooks for firewall management",
            "Created automated backup and change management workflows",
            "Built dynamic ACL update scripts",
        ]
    }),
    
    ("SECTION", "CERTIFICATIONS"),
    ("BULLETS", [
        "CCNP Security - Cisco",
        "CCNA - Cisco",
        "Azure Security Administrator Associate - Microsoft (In Progress)",
    ]),
    
    ("SECTION", "EDUCATION"),
    ("BULLETS", [
        "Master of Applied Science - Electronics & Computer Engineering, University of Windsor",
        "B.Tech - Electronics & Communication Engineering",
    ]),
    
    ("SECTION", "TECHNICAL SKILLS"),
    ("TABLE", [
        ["Category", "Skills"],
        ["Security", "Cisco ASA/FTD, FortiGate, Palo Alto, Azure Firewall, SSL Decryption, IPS/IDS"],
        ["Cloud", "Azure Firewall, NSG, ASG, VNET, UDR, NAT Gateway, Azure AD"],
        ["Automation", "Ansible, Python, Bash, Git"],
        ["Monitoring", "SolarWinds, Splunk, Azure Monitor, Nagios"],
        ["Networking", "TCP/IP, OSPF, BGP, EIGRP, VLAN, VPN"],
    ]),
]

def create_pdf(data, filename):
    """Create a PDF from resume data"""
    doc = SimpleDocTemplate(filename, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    story = []
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        alignment=TA_CENTER,
        spaceAfter=3,
    )
    section_style = ParagraphStyle(
        'Section',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor("#2c3e50"),
        borderPadding=5,
        spaceAfter=6,
        borderWidth=0,
        borderColor=colors.HexColor("#3498db"),
        borderWidthBottom=2,
    )
    
    for item in data:
        if item[0] == "HEADER":
            for key, value in item[1]:
                if key == "name":
                    p = Paragraph(value, title_style)
                    story.append(p)
                elif key == "title":
                    p = Paragraph(f"<b>{value}</b>", ParagraphStyle('SubTitle', parent=styles['Normal'], alignment=TA_CENTER, fontSize=12, textColor=colors.HexColor("#3498db")))
                    story.append(p)
                elif key == "contact":
                    p = Paragraph(value, ParagraphStyle('Contact', parent=styles['Normal'], alignment=TA_CENTER, fontSize=9, textColor=colors.gray))
                    story.append(p)
            story.append(Spacer(1, 20))
            
        elif item[0] == "SECTION":
            p = Paragraph(item[1], section_style)
            story.append(p)
            
        elif item[0] == "TEXT":
            p = Paragraph(item[1], styles['Normal'])
            story.append(Spacer(1, 10))
            
        elif item[0] == "BULLETS":
            for bullet in item[1]:
                p = Paragraph(f"• {bullet}", styles['Normal'])
                story.append(p)
            story.append(Spacer(1, 10))
            
        elif item[0] == "EXPERIENCE":
            exp = item[1]
            p = Paragraph(f"<b>{exp['title']}</b> | {exp['company']} | {exp['period']}", styles['Normal'])
            story.append(p)
            for highlight in exp['highlights']:
                p = Paragraph(f"• {highlight}", styles['Normal'])
                story.append(p)
            story.append(Spacer(1, 10))
            
        elif item[0] == "PROJECT":
            proj = item[1]
            p = Paragraph(f"<b>{proj['title']}</b>", styles['Normal'])
            story.append(p)
            for point in proj['points']:
                p = Paragraph(f"• {point}", styles['Normal'])
                story.append(p)
            story.append(Spacer(1, 8))
            
        elif item[0] == "TABLE":
            table_data = item[1]
            t = Table(table_data, colWidths=[1.5*inch, 4.5*inch])
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

def generate_all_resumes():
    """Generate all resume PDFs"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Standard Resume
    create_pdf(standard_resume, f"{OUTPUT_DIR}/Vinay_Resume_Standard.pdf")
    
    print("\n✅ All PDFs generated!")
    print(f"Location: {OUTPUT_DIR}/")

if __name__ == "__main__":
    generate_all_resumes()
