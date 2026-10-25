<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f2027,50:203a43,100:2c5364&height=200&section=header&text=Amiel%20Botbol&fontSize=52&fontColor=ffffff&animation=fadeIn&fontAlignY=34&desc=Platform%20Engineering%20%E2%80%A2%20SRE%20%E2%80%A2%20AWS%20Architecture%20%E2%80%A2%20Generative%20AI&descAlignY=56&descSize=18" alt="Amiel Botbol: Platform Engineering, SRE, AWS Architecture, Generative AI"/>

<a href="https://git.io/typing-svg">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=20&pause=900&color=36BCF7&center=true&vCenter=true&width=720&lines=Platform+Engineer+%E2%80%A2+SRE+%E2%80%A2+AWS+Architect;I+build+golden+paths+developers+actually+love;Reliability+is+a+feature%3A+SLOs+%2B+OpenTelemetry;GenAI+on+AWS+Bedrock%2C+wired+into+the+platform;Open+to+R%26D+%2F+Platform+%2F+SRE+roles" alt="Platform Engineer, SRE, AWS Architect, GenAI on AWS Bedrock"/>
</a>

<p>
  <a href="https://www.linkedin.com/in/amiel-botbol-49430a93/"><img src="https://img.shields.io/badge/LinkedIn-Let's%20talk-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>
  <a href="https://www.credly.com/badges/bdff572e-93fc-4c58-ac90-b2dbd9c96172/public_url"><img src="https://img.shields.io/badge/Credly-Verified%20Certification-FF6B00?style=for-the-badge&logo=credly&logoColor=white" alt="Credly certification"/></a>
  <img src="https://img.shields.io/badge/Open%20to-R%26D%20%7C%20Platform%20%7C%20SRE-2ea44f?style=for-the-badge" alt="Open to R&D, Platform, SRE roles"/>
  <img src="https://komarev.com/ghpvc/?username=Amidouv&style=for-the-badge&color=2c5364&label=PROFILE+VIEWS" alt="Profile views"/>
</p>

</div>

---

## 👋 TL;DR for recruiters

> **Platform Engineer & SRE with an AWS architect's mindset.** I build the internal platform that lets R&D teams ship safely on their own: paved-road CI/CD, GitOps on Kubernetes, and end-to-end observability with OpenTelemetry, Dynatrace and Splunk. Now I'm wiring **generative AI (AWS Bedrock, Claude)** into that platform, so operations get smarter and developers move faster.

```yaml
amiel:
  roles: [Platform Engineer, Site Reliability Engineer, AWS Solutions Architect]
  i_build:
    - Internal developer platforms and golden paths (self-service, secure by default)
    - Kubernetes + GitOps delivery with ArgoCD, Jenkins and GitHub Actions
    - Observability with OpenTelemetry, Dynatrace, Splunk and Prometheus
    - GenAI features and AI-assisted operations on AWS Bedrock
  i_care_about: [Developer experience, SLOs and error budgets, Cost-aware cloud design, Automation over toil]
  looking_for: R&D, Platform, SRE or Cloud Architecture teams that ship
```

<!-- TIP: add 2-3 quantified wins here. Numbers beat adjectives with recruiters, e.g.
- ⚡ Cut CI pipeline time from 40 min to 12 min by parallelising Jenkins stages
- 📉 Reduced MTTR by X% after rolling out OpenTelemetry tracing into Dynatrace
- 💸 Cut AWS spend X% with right-sizing, Graviton and spot capacity
- 🚀 Moved N services to EKS with ArgoCD GitOps, zero downtime
-->

## 🧭 What I bring to an R&D team

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>🏗️ Platform Engineering</h3>
      <ul>
        <li>Internal developer platform and <b>golden paths</b>: from repo to production in self-service</li>
        <li><b>Kubernetes</b> and <b>Docker</b> as the runtime, <b>ArgoCD</b> GitOps as the delivery contract</li>
        <li>Reusable <b>CI/CD</b> templates in Jenkins and GitHub Actions</li>
        <li>Platform as a product: docs, guardrails, and developer experience first</li>
      </ul>
    </td>
    <td width="50%" valign="top">
      <h3>🛡️ Site Reliability Engineering</h3>
      <ul>
        <li><b>SLOs, SLIs and error budgets</b> that drive release decisions</li>
        <li>Incident response, on-call and <b>blameless postmortems</b></li>
        <li>Toil reduction through automation (Python, Bash)</li>
        <li>Capacity planning and resilience on Linux / RHEL</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>☁️ AWS Solutions Architecture</h3>
      <ul>
        <li>Designs aligned to the <b>AWS Well-Architected</b> pillars</li>
        <li>Multi-account, least-privilege IAM, keyless CI via <b>OIDC</b></li>
        <li>High availability across AZs, with cost and performance in mind</li>
        <li>Containers on AWS, from build to observability</li>
      </ul>
    </td>
    <td width="50%" valign="top">
      <h3>🔭 Observability</h3>
      <ul>
        <li><b>OpenTelemetry</b> as the vendor-neutral standard for traces, metrics and logs</li>
        <li><b>Dynatrace</b> for full-stack APM and AI-driven root cause</li>
        <li><b>Splunk</b> for log analytics, dashboards and alerting</li>
        <li><b>Prometheus</b> for Kubernetes and service metrics</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <h3>🤖 Generative AI on the platform</h3>
      <ul>
        <li><b>AWS Bedrock</b> and the <b>Claude</b> API to add LLM features to products and to internal tooling</li>
        <li>AI-assisted operations: summarising incidents, logs and change history so engineers act faster</li>
        <li>Agentic development with <b>Claude Code</b>; this very page is maintained by an AI pipeline (see below)</li>
      </ul>
    </td>
  </tr>
</table>

## 🗺️ How I design a platform

```mermaid
flowchart LR
    Dev([👩‍💻 Developer]) -->|git push| GH[GitHub]
    GH --> CI[CI: Jenkins / GitHub Actions<br/>build • test • scan]
    CI -->|image| ECR[(Amazon ECR)]
    CI -->|manifest PR| GitOps[GitOps repo]
    GitOps --> Argo[ArgoCD]
    Argo --> EKS[Kubernetes on AWS]
    EKS -->|OpenTelemetry| OTel[OTel Collector]
    OTel --> DT[Dynatrace<br/>APM + root cause]
    OTel --> SPL[Splunk<br/>logs + alerts]
    OTel --> PROM[Prometheus<br/>SLO metrics]
    DT & SPL & PROM --> AI[🤖 AWS Bedrock<br/>AI incident summaries]
    AI -->|insights| Dev
```

## 🛠️ Tech stack

<p align="center">
  <img src="https://skillicons.dev/icons?i=aws,kubernetes,docker,linux,redhat,jenkins,githubactions,prometheus,git&perline=9" alt="Platform stack"/>
  <br/>
  <img src="https://skillicons.dev/icons?i=python,ts,js,html,css,bash,perl,selenium&perline=8" alt="Languages and tools"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/AWS%20Bedrock-GenAI-FF9900?style=for-the-badge&logo=amazonwebservices&logoColor=white" alt="AWS Bedrock"/>
  <img src="https://img.shields.io/badge/Dynatrace-APM-1496FF?style=for-the-badge&logo=dynatrace&logoColor=white" alt="Dynatrace"/>
  <img src="https://img.shields.io/badge/Splunk-Observability-000000?style=for-the-badge&logo=splunk&logoColor=white" alt="Splunk"/>
  <img src="https://img.shields.io/badge/OpenTelemetry-Tracing-425CC7?style=for-the-badge&logo=opentelemetry&logoColor=white" alt="OpenTelemetry"/>
  <br/>
  <img src="https://img.shields.io/badge/ArgoCD-GitOps-EF7B4D?style=for-the-badge&logo=argo&logoColor=white" alt="ArgoCD"/>
  <img src="https://img.shields.io/badge/SRE-SLOs%20%26%20Error%20Budgets-6E40C9?style=for-the-badge" alt="SRE"/>
  <img src="https://img.shields.io/badge/Claude-AI-D97757?style=for-the-badge&logo=anthropic&logoColor=white" alt="Claude"/>
  <img src="https://img.shields.io/badge/Claude%20Code-Agentic%20Dev-191919?style=for-the-badge&logo=anthropic&logoColor=white" alt="Claude Code"/>
</p>

## 🤖 Live, AI-generated: what I'm building right now

> Every Monday a GitHub Action reads my latest public activity and asks an LLM to summarise it, on **AWS Bedrock** (keyless, via OIDC) or the **Claude API**. Platform thinking applied to my own profile: automated, observable, zero toil. Source: [`scripts/update_readme.py`](scripts/update_readme.py) · [`workflow`](.github/workflows/update-readme.yml)

<!-- AI-SUMMARY:START -->
Currently focused on **platform engineering with generative AI**: building self-service delivery on **Kubernetes** and **AWS**, instrumenting services with **OpenTelemetry**, and adding LLM features through **AWS Bedrock** and **Claude Code**.
<!-- AI-SUMMARY:END -->

<details>
<summary><b>⚡ Recent public activity</b> (auto-updated)</summary>

<!-- ACTIVITY:START -->
- Profile README upgraded with an AI-generated weekly summary
<!-- ACTIVITY:END -->

</details>

## 📊 GitHub at a glance

<p align="center">
  <img height="165" src="https://github-readme-stats.vercel.app/api?username=Amidouv&show_icons=true&include_all_commits=true&count_private=true&theme=tokyonight&hide_border=true" alt="GitHub stats"/>
  <img height="165" src="https://github-readme-stats.vercel.app/api/top-langs/?username=Amidouv&layout=compact&theme=tokyonight&hide_border=true" alt="Top languages"/>
</p>

<p align="center">
  <img src="https://streak-stats.demolab.com?user=Amidouv&theme=tokyonight&hide_border=true" alt="GitHub streak"/>
</p>

<p align="center">
  <img width="95%" src="https://github-readme-activity-graph.vercel.app/graph?username=Amidouv&theme=tokyo-night&hide_border=true&area=true" alt="Contribution activity graph"/>
</p>

## 📫 Let's build something reliable

Hiring for **Platform Engineering, SRE, Cloud Architecture or R&D**? I'd love to hear what your team is building and where it hurts.
The fastest way to reach me is **[LinkedIn](https://www.linkedin.com/in/amiel-botbol-49430a93/)**.

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:2c5364,50:203a43,100:0f2027&height=100&section=footer" width="100%" alt=""/>
