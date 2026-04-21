PYTHON ?= python3
VERSION ?= v0.2.0
PLAN ?= examples/sample-launch-plan.md
OUTPUT ?= dist/index.html
PROJECT ?= AI 产品发布网页演示
AUDIENCE ?= 技术决策者
STYLE ?= neo-luxury
BRAND ?= LivePPT
README_INPUT ?= README.md
DOCX_INPUT ?= input.docx
PPTX_INPUT ?= input.pptx

.PHONY: help install-deps validate render-html build-showcase build-from-readme convert-docx convert-pptx release-note demo-gif distribution-pack

help:
	@echo "LivePPT CLI Targets:"
	@echo "  make help                 - Show this help"
	@echo "  make install-deps         - Install Python dependencies"
	@echo "  make validate             - Run smoke tests"
	@echo "  make render-html          - Render Markdown plan to HTML"
	@echo "  make build-showcase       - Generate plan + render HTML"
	@echo "  make build-from-readme    - Clean README + render HTML"
	@echo "  make convert-docx         - Convert Word .docx to HTML"
	@echo "  make convert-pptx         - Convert PowerPoint .pptx to HTML"
	@echo "  make release-note         - Generate release notes"
	@echo "  make demo-gif             - Generate demo GIF"
	@echo "  make distribution-pack    - Generate distribution pack"

install-deps:
	$(PYTHON) -m pip install -r requirements.txt

validate:
	$(PYTHON) scripts/validate_skill.py

render-html:
	$(PYTHON) scripts/render_plan_to_html.py $(PLAN) --output $(OUTPUT) --theme $(STYLE) --brand "$(BRAND)"

build-showcase:
	$(PYTHON) scripts/build_showcase.py --project "$(PROJECT)" --audience "$(AUDIENCE)" --style $(STYLE) --brand "$(BRAND)" --plan-output $(PLAN) --html-output $(OUTPUT)

build-from-readme:
	$(PYTHON) scripts/build_from_readme.py $(README_INPUT) --output $(OUTPUT) --theme $(STYLE) --brand "$(BRAND)"

convert-docx:
	$(PYTHON) scripts/convert_from_docx.py $(DOCX_INPUT) --output $(OUTPUT) --theme $(STYLE) --brand "$(BRAND)"

convert-pptx:
	$(PYTHON) scripts/convert_from_pptx.py $(PPTX_INPUT) --output $(OUTPUT) --theme $(STYLE) --brand "$(BRAND)"

release-note:
	$(PYTHON) scripts/generate_release_note.py --version $(VERSION)

demo-gif:
	$(PYTHON) scripts/generate_demo_gif.py --output assets/demo.gif

distribution-pack:
	$(PYTHON) scripts/generate_distribution_pack.py --version $(VERSION)
