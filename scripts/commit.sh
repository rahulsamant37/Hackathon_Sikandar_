#!/bin/bash

# Script to help create conventional commits

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Commit types
TYPES=("feat" "fix" "docs" "style" "refactor" "perf" "test" "chore" "ci")
TYPES_DESC=(
    "A new feature"
    "A bug fix"
    "Documentation only changes"
    "Changes that do not affect the meaning of the code"
    "A code change that neither fixes a bug nor adds a feature"
    "A code change that improves performance"
    "Adding missing tests or correcting existing tests"
    "Changes to the build process or auxiliary tools"
    "Changes to CI configuration files and scripts"
)

# Common scopes
SCOPES=("backend" "frontend" "api" "auth" "courses" "modules" "content" "analytics" "ai" "infra" "db" "ui" "docs" "tests" "deps" "config")

# Print header
echo -e "${BLUE}=== Conventional Commit Helper ===${NC}"
echo "This script helps you create a commit message following the Conventional Commits specification."
echo "Learn more: https://www.conventionalcommits.org/"
echo ""

# Select commit type
echo -e "${YELLOW}Select commit type:${NC}"
for i in "${!TYPES[@]}"; do
    echo -e "$i: ${GREEN}${TYPES[$i]}${NC} - ${TYPES_DESC[$i]}"
done

read -p "Enter type number: " type_num
if [[ ! $type_num =~ ^[0-9]+$ ]] || [ $type_num -ge ${#TYPES[@]} ]; then
    echo -e "${RED}Invalid selection. Exiting.${NC}"
    exit 1
fi

TYPE=${TYPES[$type_num]}

# Select scope
echo -e "\n${YELLOW}Select scope (or enter custom scope):${NC}"
for i in "${!SCOPES[@]}"; do
    echo -e "$i: ${GREEN}${SCOPES[$i]}${NC}"
done
echo -e "c: ${GREEN}custom scope${NC}"
echo -e "n: ${GREEN}no scope${NC}"

read -p "Enter scope option: " scope_option

if [ "$scope_option" = "c" ]; then
    read -p "Enter custom scope: " SCOPE
elif [ "$scope_option" = "n" ]; then
    SCOPE=""
elif [[ $scope_option =~ ^[0-9]+$ ]] && [ $scope_option -lt ${#SCOPES[@]} ]; then
    SCOPE=${SCOPES[$scope_option]}
else
    echo -e "${RED}Invalid selection. Exiting.${NC}"
    exit 1
fi

# Enter subject
echo -e "\n${YELLOW}Enter commit subject (short description):${NC}"
read -p "> " SUBJECT

if [ -z "$SUBJECT" ]; then
    echo -e "${RED}Subject cannot be empty. Exiting.${NC}"
    exit 1
fi

# Enter body (optional)
echo -e "\n${YELLOW}Enter commit body (optional, press Enter to skip):${NC}"
read -p "> " BODY

# Enter footer (optional)
echo -e "\n${YELLOW}Enter commit footer (optional, press Enter to skip):${NC}"
echo "Example: 'Closes #123' or 'BREAKING CHANGE: <description>'"
read -p "> " FOOTER

# Build commit message
if [ -z "$SCOPE" ]; then
    COMMIT_MSG="$TYPE: $SUBJECT"
else
    COMMIT_MSG="$TYPE($SCOPE): $SUBJECT"
fi

if [ ! -z "$BODY" ]; then
    COMMIT_MSG="$COMMIT_MSG\n\n$BODY"
fi

if [ ! -z "$FOOTER" ]; then
    COMMIT_MSG="$COMMIT_MSG\n\n$FOOTER"
fi

# Preview commit message
echo -e "\n${BLUE}=== Commit Message Preview ===${NC}"
echo -e "$COMMIT_MSG"
echo -e "${BLUE}=============================${NC}"

# Confirm and commit
echo -e "\n${YELLOW}Do you want to commit with this message? (y/n)${NC}"
read -p "> " CONFIRM

if [ "$CONFIRM" = "y" ] || [ "$CONFIRM" = "Y" ]; then
    echo -e "$COMMIT_MSG" | git commit -F -
    echo -e "${GREEN}Commit created successfully!${NC}"
else
    echo -e "${RED}Commit cancelled.${NC}"
    exit 0
fi
