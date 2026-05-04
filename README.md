# Django TeamFlow

Django TeamFlow is a learning-focused Django backend project.

The goal of this repository is to help learners understand how a real Django backend grows step by step, starting from simple models and app structure before moving into APIs, authentication, permissions, services, billing, and production-oriented patterns.

This is not just a tutorial project. It is designed to show how backend ideas connect together in a realistic system.

## What This Project Is

Django TeamFlow is a team-based project management backend.

The system is built around a simple domain:

- teams
- team memberships
- projects
- tasks

A team can have many members.  
A team can own many projects.  
A project can have many tasks.  
Tasks can be assigned to team members.

This makes the project useful for learning Django relationships, app boundaries, and data modeling.

## Current Phase

Current phase: **Phase 1 — Core Models and App Structure**

This phase focuses on the foundation of the project.

The main goal is to understand:

- why Django projects are split into apps
- how models represent business concepts
- how relationships work between models
- how to keep app responsibilities clear
- how to design a simple but realistic backend data model

This phase does not focus on APIs, permissions, authentication, billing, or admin customization yet.

Those topics will be introduced later.

## Beginner Learning Path

This project may contain a custom user model, but custom users and authentication are not the focus of the beginner phase. It is okay if you don't understand the `users` models. 

For this reason, the beginner path focuses first on the project domain:

Teams → Memberships → Projects → Tasks

## Main Apps

The project is organized into separate Django apps.

Current important apps:

- `teams`
- `projects`
- `users`
- `core`
- `billing`

For this phase, the main learning focus is:

- `teams`
- `projects`

The `users` app exists because teams need members, but custom authentication is not explained deeply yet.

## Teams App

The `teams` app represents groups of people working together.

It contains two main models:

- `Team`
- `TeamMembership`

## Team

A `Team` is a workspace or group.

A team can have many members and many projects.

Example teams:

- Design Team
- Marketing Team
- Engineering Team

The team model stores simple information such as:

- `name`
- `description`
- `created_at`
- `updated_at`

## TeamMembership

A `TeamMembership` connects a user to a team.

This model exists because the relationship between a user and a team has extra meaning.

A user is not just connected to a team.  
The user also has a role inside that team.

Example roles:

- `owner`
- `admin`
- `member`

This allows one user to have different roles in different teams.

Example:

- A user can be an owner in Team A.
- The same user can be a member in Team B.

This is why the role belongs on `TeamMembership`, not directly on the user.

## Projects App

The `projects` app represents work managed by teams.

It contains two main models:

- `Project`
- `Task`

## Project

A `Project` belongs to one team.

A team can have many projects.

Example projects:

- Website Redesign
- Mobile App Launch
- Internal CRM

The project model stores information such as:

- `team`
- `name`
- `description`
- `start_date`
- `end_date`
- `created_at`
- `updated_at`

The `end_date` is optional because not every project has a known end date when it is created.

## Task

A `Task` belongs to one project.

A task can be assigned to one or more team members.

The task model stores information such as:

- `project`
- `assigned_members`
- `title`
- `description`
- `start_date`
- `end_date`
- `is_done`
- `created_at`
- `updated_at`

Tasks are assigned to `TeamMembership`, not directly to a user.

This is intentional.

A task belongs to a project.  
A project belongs to a team.  
So the task should be assigned to someone as a member of that team.

This keeps the business meaning clearer.

## Important Relationships

The current data model teaches these Django relationship types:

- `ForeignKey`
- `ManyToManyField`
- many-to-many relationship with a through model
- one-to-many relationships
- reverse relationships
- unique constraints

The full relationship structure is:

- `Team`
  - has many `TeamMembership` records
  - has many `User` records through `TeamMembership`
  - has many `Project` records

- `TeamMembership`
  - belongs to one `Team`
  - belongs to one `User`
  - stores the user's role inside that team
  - can be assigned to many `Task` records

- `User`
  - has many `TeamMembership` records
  - has many `Team` records through `TeamMembership`

- `Project`
  - belongs to one `Team`
  - has many `Task` records

- `Task`
  - belongs to one `Project`
  - has many assigned `TeamMembership` records
