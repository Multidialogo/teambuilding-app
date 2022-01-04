// REQUIRES JQUERY

class FormsetManager {
    constructor(modelName) {
        this.modelName = modelName;
    }

    getTotalFormsMetaId() {
        return 'id_' + this.modelName + '_set-TOTAL_FORMS';
    }

    getTotalFormsCount() {
        return $('#' + this.getTotalFormsMetaId()).val();
    }

    setTotalFormsCount(count) {
        return $('#' + this.getTotalFormsMetaId()).val(count);
    }

    getFormDeleteCheckboxId(index) {
        return 'id_' + this.modelName + '_set-' + index + '-DELETE';
    }

    updateMeta(forms) {
        let count = $(forms).length;
        this.setTotalFormsCount(count);
    }

    update(metaContainer, formsContainer) {
        let forms = $(formsContainer).find('[data-formset_form=""]')
        this.updateMeta(forms);

        let displayIndex = 0;
        $(forms).each(function (index, form) {
                let deleteCheckbox = $('#' + this.getFormDeleteCheckboxId(index));
                let markedForDelete = $(deleteCheckbox).is(':checked');

                if (!markedForDelete) {
                    displayIndex++;

                    let displayCountElement = $(form).find('[data-formset_form_display_count=""]').first();
                    $(displayCountElement).html('#' + displayIndex);
                } else {
                    $(form).hide();
                }
            }.bind(this)
        );
    }

    markFormForDelete(index) {
        let deleteCheckbox = $('#' + this.getFormDeleteCheckboxId(index));
        $(deleteCheckbox).prop('checked', true);
    }

    onFormAddNewClick(button) {
        let parentMetaContainer = $(button).closest('[data-formset_meta_container=""]');
        let formsContainer = $(parentMetaContainer).find('[data-formset_forms_container=""]').first();
        let emptyFormContainer = $(parentMetaContainer).find('[data-formset_empty_form_container=""]').first();
        let nextIndex = this.getTotalFormsCount();

        $(formsContainer).append($(emptyFormContainer).html().replace(/__prefix__/g, nextIndex));
        this.update(parentMetaContainer, formsContainer);
    }

    onFormRemoveClick(button) {
        let parentForm = $(button).closest('[data-formset_form=""]');
        let parentMetaContainer = $(button).closest('[data-formset_meta_container=""]');
        let formsContainer = $(parentMetaContainer).find('[data-formset_forms_container=""]').first();
        let prefixHolder = $(parentForm).find('[data-formset_form_prefix_holder=""]').first();
        let index = $(prefixHolder).attr('data-formset_form_prefix');

        this.markFormForDelete(index);

        $(parentForm).hide();
        this.update(parentMetaContainer, formsContainer);
    }
}

class FormsetManagerDispatcher {
    onFormAddNewClick(button, uniqueName) {
        let formsetManager = new FormsetManager(uniqueName);
        return formsetManager.onFormAddNewClick(button);
    }

    onFormRemoveClick(button, uniqueName) {
        let formsetManager = new FormsetManager(uniqueName);
        return formsetManager.onFormRemoveClick(button);
    }
}

function onFormsetFormAddNewClick(button, modelName) {
    let formsetManagerDispatcher = new FormsetManagerDispatcher();
    formsetManagerDispatcher.onFormAddNewClick(button, modelName);
}

function onFormsetFormRemoveClick(button, modelName) {
    let formsetManagerDispatcher = new FormsetManagerDispatcher();
    formsetManagerDispatcher.onFormRemoveClick(button, modelName);
}
